# 深入解析 LCEL 架构：`RunnableParallel` vs `RunnablePassthrough.assign` 的核心抉择

在构建 LangChain (LCEL) 管道时，处理数据流（通常是 Dictionary）的组装和并发计算是家常便饭。很多开发者会发现，`RunnableParallel` 和 `RunnablePassthrough.assign()` 似乎都能用来“并发地为字典添加新属性”。

但作为架构师，我们需要理解它们底层设计哲学的根本差异：**一个是“数据塑形与重建（Rebuild）”，一个是“上下文增量补充（Append）”。**

本文将从结构纯洁性、输入多态性以及并发陷阱三个维度，彻底拆解两者的使用场景。

---

## 1. `RunnablePassthrough.assign()`：锦上添花的“增量补充”

`.assign()` 是一种专门设计的语法糖，其底层逻辑等同于 Python 的 `dict.update()`。

**核心逻辑：** 强制保留输入字典的所有原有数据，并将新的计算结果无缝合并（Merge）进去。

### 适用场景：管道中途的上下文传递
当你处于整个 LCEL 链路的中游，上游传来的字典中已经包含了你需要的各种变量，你只是想再查一个数据库，顺手把新数据塞进去，此时闭眼选 `.assign()`。

```python
from langchain_core.runnables import RunnablePassthrough

# 上游输入: {"user_id": 123, "query": "如何学习 AI？", "history": "..."}
chain = RunnablePassthrough.assign(
    # 核心优势：原有的 user_id, query, history 会自动保留，向下游传递！
    retrieved_docs=lambda x: fetch_docs(x["query"])
)
# 输出: 包含上述 4 个 key 的大字典
```

### ⚠️ 进阶必知：并发陷阱
`.assign()` 参数内部的任务是**绝对并发**的（底层依然借用了 `RunnableParallel`），但多个 `.assign()` 的链式调用是**绝对串行**的。

```python
# ✅ 正确写法：A 和 B 并发执行，极大地节省 TTFT
chain = RunnablePassthrough.assign(
    A=slow_task_A, 
    B=slow_task_B
)

# ❌ 错误写法（新手常犯）：A 执行完后，B 才开始执行！极其拖慢响应时间
chain = RunnablePassthrough.assign(A=slow_task_A) \
                           .assign(B=slow_task_B)
```

---

## 2. `RunnableParallel`：推倒重来的“数据塑形”

如果说 `.assign()` 是做加法，那么 `RunnableParallel` 则是真正的**白纸作画**。它会丢弃原有的结构，完全根据你定义的分支重新组装出一个全新的字典。

### 核心优势 1：结构纯洁性（做减法）
在复杂的微服务或 Agent 编排中，上游传来的字典可能混杂了大量垃圾数据（如 `session_id`, `tmp_cache`, 各种中间变量）。如果你使用 `.assign()`，这些“狗皮膏药”会一路跟着数据流走到最后。如果把它们全丢给大模型，不仅浪费大量 Token，还极易引发 LLM 的幻觉。

使用 `RunnableParallel` 可以完美**截断**这些垃圾数据：

```python
from langchain_core.runnables import RunnableParallel

# 上游输入: {"raw_html": "...", "tmp_token": "abc", "query": "价格"}
clean_chain = RunnableParallel(
    # 手动重组，只保留干货！垃圾数据 tmp_token 直接被丢弃。
    context=lambda x: clean_html(x["raw_html"]),
    question=lambda x: x["query"]
)
# 输出极其纯洁: {"context": "...", "question": "价格"} -> 完美喂给 Prompt
```

### 核心优势 2：多态输入（突破 Dict 的限制）
`.assign()` 的前提是**输入必须是个 Dict**。如果用户的原始输入是一段单纯的字符串，调用 `.assign()` 会当场抛出异常。

`RunnableParallel` 是把**非 Dict 转化为 Dict** 的第一道关卡（Fan-out 扇出节点）：

```python
from langchain_core.runnables import RunnablePassthrough

# 用户原始输入就是一个 String: "明天广州天气如何？"
start_chain = RunnableParallel(
    question=RunnablePassthrough(), # 拿到原字符串
    history=get_history             # 并发查询历史记录
)
# 瞬间把一维文本展平成了二维字典: {"question": "明天广州天气如何？", "history": "..."}
```

---

## 3. 终极架构总结选型指南

1. **管道源头（入口层）**：
   👉 使用 `RunnableParallel`。将用户的一维输入（String）或复杂请求转化为结构化的 Dict。
2. **管道中途（业务逻辑层）**：
   👉 使用 `.assign()`。在不破坏原有上下文的情况下，无痛注入新的业务字段。
3. **Prompt 组装前（模型前置层）**：
   👉 强烈推荐使用 `RunnableParallel`。作为数据进入大模型前的最后一道“安检清洗”，强制丢弃所有无用变量，确保 Prompt 的精确性和 Token 利用率。
   
**LangSmith 监控视角**：在 LangSmith 的 Tracing 面板中，直接声明的 `RunnableParallel` 会展示为非常清晰的并列 DAG 节点，便于排查并发瓶颈；而 `.assign()` 会被多包裹一层，视图相对冗长。