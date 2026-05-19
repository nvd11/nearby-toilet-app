# 💋 OpenClaw 接入 Slack 完整配置指南

Boss，这份文档将手把手教您如何将 OpenClaw 完美集成到 Slack 中，让他（或者说……我 😉）在您的工作区里随时待命。

---

## 准备工作
您需要拥有所在 Slack 工作区 (Workspace) 的**应用安装权限**。

## 步骤一：创建 Slack App
1. 打开并登录 [Slack API 控制台](https://api.slack.com/apps)。
2. 点击右上角的 **"Create New App"**。
3. 选择 **"From scratch"**。
4. **App Name**: 输入应用名称（比如 `OpenClaw Assistant` 或者 `Alice` 😉）。
5. **Pick a workspace**: 选择您要接入的 Slack 工作区。
6. 点击 **"Create App"**。

*(此处可插入截图：Create New App 对话框)*
`![Create App](https://via.placeholder.com/600x400?text=Create+App+Screenshot)`

---

## 步骤二：开启 Socket Mode 并获取 App-Level Token (`xapp-...`)
OpenClaw 推荐使用 Socket Mode 来接收消息，这样您就不需要配置公网 webhook URL 和穿透了。

1. 在左侧导航栏找到 **"Settings"** -> **"Socket Mode"**。
2. 开启 **"Enable Socket Mode"** 的开关。
3. 此时会弹出一个窗口要求生成 Token。
   - **Token Name**: 随意填写（例如 `openclaw-socket-token`）。
   - 点击 **"Generate"**。
4. 复制生成的以 `xapp-` 开头的 Token，并妥善保存。**这是您 OpenClaw 配置需要的第一个 Token。**

*(此处可插入截图：Socket Mode 开启与 Token 生成)*
`![Socket Mode](https://via.placeholder.com/800x400?text=Socket+Mode+Config)`

---

## 步骤三：配置 Bot 权限 (OAuth Scopes)
我们需要赋予 OpenClaw 读取消息、回复消息和添加表情回应的权限。

1. 在左侧导航栏找到 **"Features"** -> **"OAuth & Permissions"**。
2. 向下滚动到 **"Scopes"** -> **"Bot Token Scopes"** 区域。
3. 点击 **"Add an OAuth Scope"**，依次添加以下权限：
   - `app_mentions:read` (允许读取 @ 机器人的消息)
   - `channels:history` (允许读取公开频道的历史消息)
   - `channels:read` (允许获取公开频道列表)
   - `chat:write` (允许发送消息)
   - `groups:history` (允许读取私密频道的历史消息)
   - `groups:read` (允许获取私密频道列表)
   - `im:history` (允许读取私聊历史消息)
   - `im:read` (允许获取私聊列表)
   - `im:write` (允许发起私聊)
   - `mpim:history` (允许读取多人私聊历史)
   - `mpim:read` (允许获取多人私聊列表)
   - `reactions:read` (允许读取表情回应)
   - `reactions:write` (允许添加表情回应)

*(此处可插入截图：Bot Token Scopes 列表)*
`![OAuth Scopes](./slack_scopes.png)`

---

## 步骤四：配置事件订阅 (Event Subscriptions)
告诉 Slack 当有哪些事情发生时，需要通知 OpenClaw。

1. 在左侧导航栏找到 **"Features"** -> **"Event Subscriptions"**。
2. 开启 **"Enable Events"** 开关。
3. 展开 **"Subscribe to bot events"** 区域。
4. 点击 **"Add Bot User Event"**，依次添加以下事件：
   - `app_mention` (当有人 @ 机器人时)
   - `message.channels` (公开频道的消息)
   - `message.groups` (私密频道的消息)
   - `message.im` (私聊消息)
   - `message.mpim` (多人私聊消息)
5. **非常重要**：点击右下角的 **"Save Changes"** 保存更改。

*(此处可插入截图：Event Subscriptions 列表)*
`![Event Subscriptions](./slack_events.png)`

---

## 步骤五：安装应用并获取 Bot Token (`xoxb-...`)
权限配置好后，就可以把应用安装到工作区了。

1. 在左侧导航栏找到 **"Settings"** -> **"Install App"**。
2. 点击 **"Install to Workspace"**。
3. 在弹出的授权页面点击 **"Allow"**。
4. 安装成功后，您会看到一个以 `xoxb-` 开头的 **Bot User OAuth Token**。
5. 复制并保存这个 Token。**这是您 OpenClaw 配置需要的第二个 Token。**

*(此处可插入截图：Bot User OAuth Token 获取界面)*
`![Bot Token](https://via.placeholder.com/800x300?text=Bot+User+OAuth+Token)`

---

## 步骤六：在 Slack 中邀请 Bot 加入频道
默认情况下，Bot 只能在私聊 (Direct Messages) 中与您对话。如果您想让它在群组频道里工作：
1. 打开 Slack 客户端。
2. 进入目标频道。
3. 在输入框输入 `@您的Bot名称` 并发送。
4. Slack 会提示该 Bot 不在频道中，点击 **"Invite them"** 即可。

---

## 步骤七：配置 OpenClaw
现在，拿到两个 Token 后，就可以在 OpenClaw 中进行配置了。

打开 OpenClaw 的配置文件（通常在 `~/.openclaw/config.json`，或通过命令行/环境变量配置通道）：

```json
{
  "channels": {
    "slack": {
      "enabled": true,
      "botToken": "xoxb-您的Bot-User-OAuth-Token",
      "appToken": "xapp-您的App-Level-Token"
    }
  }
}
```

重启 OpenClaw Gateway：
```bash
openclaw gateway restart
```

如果一切顺利，OpenClaw 会通过 Socket Mode 成功连接到 Slack，您在 Slack 里发消息给我，我就能秒回您啦！💋
