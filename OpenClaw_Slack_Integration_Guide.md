# 🚀 OpenClaw 无缝接入 Slack 全图文实战指南

本文档详细记录了如何将 OpenClaw AI 助手无缝集成到 Slack 工作区，采用最新的 **Socket Mode（长连接模式）**，无需公网 IP 和复杂的 Webhook 验证即可实现双向通讯。

> 💡 **背景备注**：这份文档基于老板（Jason）与 AI 秘书（Alice）于 2026年3月16日 在 GCP 云端服务器的实战踩坑经验总结。特别是针对 `missing_scope` 等权限拦截问题给出了明确的避坑指南。

---

## 🛠️ 核心准备
- Slack 工作区管理员权限
- 运行中的 OpenClaw 实例（Gateway）

---

## Step 1: 创建 Slack App
1. 访问 [Slack API 控制台](https://api.slack.com/apps)。
2. 点击右上角的 **Create New App** -> 选择 **From scratch**。
3. 填入 App Name（比如 `OpenClaw-Alice`），并选择您的 Workspace。

> 📸 *[此处插入截图：Create an app 对话框，填入名称并选择工作区]*

---

## Step 2: 开启 Socket Mode (获取 App-Level Token)
由于 OpenClaw 默认使用 WebSocket 长连接模式来接收消息（不需要配置外网 Request URL），这一步必须开启。
1. 在左侧导航栏找到 **Settings -> Socket Mode**。
2. 打开 **Enable Socket Mode** 开关。
3. 弹出的对话框中，为您的 Token 命名（如 `openclaw-socket-token`），系统会自动为其添加 `connections:write` 权限。
4. 点击 Generate，**复制并保存** 生成的 **App-Level Token**（以 `xapp-` 开头）。

> 📸 *[此处插入截图：Socket Mode 开启界面与 xapp- Token 复制弹窗]*

---

## Step 3: 配置权限范围 (Bot Scopes) —— ⚠️ 实战踩坑点！
机器人在 Slack 里能干什么，全看这里给了什么权限。**如果权限给少了，OpenClaw 后台会疯狂报错 `Error: An API error occurred: missing_scope`！**

1. 左侧导航栏找到 **Features -> OAuth & Permissions**。
2. 下拉找到 **Scopes -> Bot Token Scopes**，点击 **Add an OAuth Scope**。
3. **必须添加以下核心权限**：
   - `app_mentions:read` —— 允许机器人在频道里被 @ 唤醒
   - `channels:history` / `groups:history` / `im:history` —— 允许机器人读取频道、私聊的历史消息上下文
   - `chat:write` —— **【关键！】** 允许机器人发送文本消息（没有它机器人只能看不能回）
   - `files:write` —— **【关键！】** 允许机器人上传并发送图片、视频（比如我们在后台渲染的 Veo 4K 视频或架构图，缺了这个发不出去）

> 📸 *[此处插入截图：Bot Token Scopes 配置完成后的列表清单]*

---

## Step 4: 订阅事件 (Event Subscriptions)
告诉 Slack 哪些动作发生时，需要通知我们的 OpenClaw。
1. 左侧导航栏找到 **Features -> Event Subscriptions**。
2. 打开 **Enable Events** 开关。
3. 下拉找到 **Subscribe to bot events**，添加以下事件：
   - `app_mention` (接收群聊中的 @ 消息)
   - `message.im` (接收私聊消息)
   - `message.channels` / `message.groups` (接收公开/私密频道的普通消息)
4. 点击页面右下角的 **Save Changes**。

> 📸 *[此处插入截图：Event Subscriptions 开启状态及订阅的四个核心事件]*

---

## Step 5: 安装应用并获取 Bot Token
1. 回到左侧导航栏 **Settings -> Install App**（或者回到 OAuth & Permissions 的最上方）。
2. 点击 **Install to Workspace**，并在弹出的授权页面点击 **Allow (允许)**。
3. **复制并保存** 生成的 **Bot User OAuth Token**（以 `xoxb-` 开头）。

> 📸 *[此处插入截图：OAuth Tokens for Your Workspace 页面，打码显示 xoxb- Token]*

---

## Step 6: 邀请机器人进入频道
- 在您的 Slack 客户端中，打开想要让 OpenClaw 工作的频道（Channel）。
- 在聊天框输入 `@OpenClaw-Alice` (您给机器人取的名字) 并发送。
- Slack 会提示您该机器人不在频道中，点击 **Add to Channel** 即可。

---

## Step 7: 配置 OpenClaw 网关
拿到一前一后两个 Token (`xapp-...` 和 `xoxb-...`) 后，进入部署 OpenClaw 的服务器。

通过 CLI 配置（推荐）：
```bash
# 1. 设置 Bot Token (负责发消息)
openclaw config set channels.slack.botToken "xoxb-您的BotToken"

# 2. 设置 App Token (负责建立长连接)
openclaw config set channels.slack.appToken "xapp-您的AppToken"

# 3. 开放群聊和私聊策略 (如果在内网/私人团队，可设为 open，否则建议设为 allowlist)
openclaw config set channels.slack.groupPolicy "open"
openclaw config set channels.slack.dmPolicy "open"

# 4. 启用 Slack 频道并重启 Gateway
openclaw config set channels.slack.enabled true
openclaw gateway restart
```

**验证连通性：**
运行 `openclaw gateway status` 或者去 Slack 里私聊机器人发送 `hi`。如果收到机器人的回复，配置即大功告成！🎉
