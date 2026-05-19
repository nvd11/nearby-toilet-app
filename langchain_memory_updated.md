# 深入剖析 LangChain 记忆机制：RunnableWithMessageHistory 全解与底层 I/O 揭秘

在构建聊天机器人（Chatbot）时，**“记忆”（Memory）**是核心能力之一。早期的 LangChain 使用 `ConversationChain` + `Memory` 对象来管理历史，但在 LCEL（LangChain Expression Language）时代，官方推荐使用更灵活、更解耦的 `RunnableWithMessageHistory`。

本文将以一个完整的 Python 示例为基础，深入剖析 `RunnableWithMessageHistory` 的工作原理，并独家揭秘其底层基于 AOP（面向切面编程）的拦截写入机制，以及如何在生产环境中零入侵切换到 PostgreSQL 数据库。

---

## 1. 为什么需要它？

在没有 `RunnableWithMessageHistory` 之前，手动管理对话历史通常需要以下繁琐步骤：
1. **查询**：根据 User ID 从数据库查出历史记录。
2. **拼接**：手动把历史记录塞进 Prompt 中。
3. **调用**：执行 LLM。
4. **保存**：手动把 User Input 和 AI Output 追加保存回数据库。

`RunnableWithMessageHistory` 就像一个自动化的切面（Aspect），它包装了你的 Chain，自动在后台完成了上述“查询-注入-保存”的所有工作，让你只需要关注当前轮次的交互。

---

## 2. 实战代码演示：基于内存的基础版本

以下是一个可运行的完整示例，我们先用 Python 内存字典来模拟存储：

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from src.llm.gemini_chat_model import get_gemini_llm

# 1. 定义存储：这里使用内存字典模拟数据库
store = {}

# 2. 定义工厂函数：告诉系统如何根据 session_id 获取历史对象
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 3. 初始化 LLM 和 Prompt
llm = get_gemini_llm()
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"), # <--- 关键点：预留位置
    ("human", "{input}"),
])
chain = prompt | llm

# 4. 核心包装
with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# 5. 极简的业务调用
response = with_message_history.invoke(
    {"input": "Hi! My name is Bob."},
    config={"configurable": {"session_id": "session_1"}}
)
```

---

## 3. 进阶核心揭秘：LCEL 是如何“偷偷”写入数据的？

很多具备工程经验的开发者在使用该切面时会产生一个尖锐的疑问：**参数里只有 `get_session_history()` 定义了从哪里获取历史，根本没有定义“写入到哪里（save_history）”，开发者也没有手动调用写入方法，数据是怎么存下来的？**

### 3.1 AOP 代理模式与拦截器
其实，当你调用 `with_message_history.invoke()` 时，你调用的已经不是底层大模型的原生方法了，而是被 LangChain **劫持（Intercept）**过的增强版方法。

如果用伪代码还原 `RunnableWithMessageHistory` 的底层源码，其实长这样：

```python
class RunnableWithMessageHistory:
    def invoke(self, input_dict, config):
        session_id = config["configurable"]["session_id"]
        
        # 1. 调用工厂函数，拿到历史对象（自带 I/O 能力）
        history_obj = self.get_session_history(session_id)
        
        # 2. 把历史记录拼接到 input_dict 送进 Prompt
        input_dict[self.history_messages_key] = history_obj.messages
        
        # 3. 执行真正的底层 Chain (Prompt | LLM)
        ai_response = self.runnable.invoke(input_dict)

        # 🚨 重点来了！框架在这里“偷偷地”帮你调用了 I/O 方法 🚨
        history_obj.add_user_message(input_dict[self.input_messages_key])
        history_obj.add_ai_message(ai_response)
        
        return ai_response
```
正是因为框架在底层切面中“替你负重前行”，自动调用了 `add_user_message`，你的表层业务代码才得以保持极简。这就是 AOP（面向切面编程）的魅力所在。

---

## 4. 生产环境最佳实践：零入侵切换 PostgreSQL

上面例子中使用的 `store = {}` 是**进程内内存（In-memory）**，一旦 Python 服务重启，用户就会“失忆”。
在真实的生产环境中，我们需要持久化（如 PostgreSQL 或 Redis）。

**得益于 LangChain 的 IoC（控制反转）和里氏替换原则，切换底层数据库对主业务代码是“零入侵”的！**

你**不需要修改任何 `.invoke()` 的业务代码**，只需要将工厂函数里的内存对象替换为官方的 `PostgresChatMessageHistory` 即可：

```python
# 引入 LangChain 提供的 PGSQL 历史记录类
from langchain_community.chat_message_histories import PostgresChatMessageHistory

PG_CONN_STR = "postgresql://my_user:my_password@localhost:5432/my_database"

# 👇 重点来了：只改这个工厂函数！
def get_session_history(session_id: str):
    # 直接实例化并返回一个 PostgresChatMessageHistory 对象
    # 它会自动在数据库里建表，并管理数据连接
    return PostgresChatMessageHistory(
        connection_string=PG_CONN_STR,
        session_id=session_id,
        table_name="my_chat_logs"
    )

# 👇 下面的包装和调用代码，和原来一模一样，一行都不用改！
with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# 业务照常调用
response = with_message_history.invoke(...)
```

### 底层魔法分析：
当 LCEL 切面在后台“偷偷”执行 `history_obj.add_user_message("Hi!")` 时：
1. 以前：`history_obj` 是内存对象，所以只执行 `list.append()`。
2. 现在：`history_obj` 变成了 PGSQL 实例，它重写了 `add_user_message`，底层会自动帮你拼接并执行 SQL：
   `INSERT INTO my_chat_logs (session_id, message) VALUES ('session_1', '...');`

这种将**流程控制（什么时候存取）**与**存储实现（存到哪）**彻底解耦的设计，展示了 LCEL 极其优秀的架构扩展性。