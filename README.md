# BiliGo - B站私信自动回复系统

🤖 一款基于Flask和RAG服务的B站私信AI自动回复软件

## 📋 目录

- [功能介绍](#功能介绍)
- [快速开始](#快速开始)
- [系统要求](#系统要求)
- [配置说明](#配置说明)
- [API文档](#api文档)
- [常见问题](#常见问题)
- [致谢与反馈](#致谢与反馈)

## ✨ 功能介绍

### 核心功能

- **🤖 AI智能回复**: 集成RAG服务和Claude AI，提供智能化回复
- **⚡ 实时监控**: 持续监控B站私信，实时处理和回复
- **📝 关键词匹配**: 支持规则模式和AI模式混合使用
- **👥 关注者检测**: 自动检测新关注和取消关注
- **🌐 Web管理界面**: Flask提供的Web UI进行配置和监控
- **📊 日志系统**: 完整的操作日志记录和查看
- **🔄 自动降级**: AI服务异常时自动降级到规则模式

### 高级特性

- 支持文字和图片回复
- 多轮对话上下文管理
- 灵活的发送延迟控制
- 关注者状态监控
- 配置导入导出
- 规则批量管理

## 🚀 快速开始

### 系统要求

- Python 3.8+
- Flask
- Requests
- (可选) Anthropic SDK for Claude AI

### 安装步骤

1. **克隆仓库**

```bash
# HTTPS
git clone https://github.com/Wu-ChengLiang/BiliGo.git

# SSH
git clone git@github.com:Wu-ChengLiang/BiliGo.git

cd BiliGo
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **配置凭证**

```bash
# 复制模板配置文件
cp config.json.template config.json

# 编辑配置文件，填入你的B站凭证
# SESSDATA 和 bili_jct 可以从浏览器F12开发者工具中获取
```

4. **启动应用**

```bash
python app.py
```

5. **访问Web界面**

在浏览器中访问: **http://localhost:4999**

## ⚙️ 配置说明

### config.json 配置项

#### 登录信息
- `sessdata`: B站登录会话数据
- `bili_jct`: B站CSRF令牌

#### AI配置
- `ai_agent_enabled`: 是否启用AI回复 (true/false)
- `ai_agent_mode`: 回复模式 ("rule" 规则模式 / "ai" AI模式)
- `rag_service_url`: RAG服务地址 (默认: http://127.0.0.1:8000)
- `ai_use_fallback`: AI失败是否降级到规则模式

#### 回复配置
- `default_reply_enabled`: 是否启用默认回复
- `default_reply_message`: 默认回复文字
- `default_reply_type`: 回复类型 ("text" 文字 / "image" 图片)

#### 关注者功能
- `follow_reply_enabled`: 新关注时是否回复
- `follow_reply_message`: 关注欢迎文字
- `unfollow_reply_enabled`: 取消关注时是否回复
- `unfollow_reply_message`: 取消关注告别文字

#### 时间间隔
- `message_check_interval`: 消息检查间隔 (秒，默认: 0.05)
- `send_delay_interval`: 消息发送间隔 (秒，默认: 1.0)
- `follow_check_interval`: 关注者检查间隔 (秒，默认: 30)

### 环境变量

系统支持通过环境变量覆盖配置文件中的敏感信息：

```bash
# B站登录凭证
export BILI_SESSDATA="your_sessdata"
export BILI_JCT="your_bili_jct"

# AI服务配置
export RAG_SERVICE_URL="http://127.0.0.1:8000"
export ANTHROPIC_API_KEY="your_api_key"  # Claude API密钥
export ZHIPU_API_KEY="your_api_key"      # 智谱API密钥
```

## 📚 API文档

### 配置管理

```bash
# 获取当前配置
GET /api/config

# 更新配置
POST /api/config
Content-Type: application/json
{
  "default_reply_message": "新的回复文字"
}
```

### 规则管理

```bash
# 获取所有规则
GET /api/rules

# 更新规则
POST /api/rules
Content-Type: application/json
{
  "rules": [
    {
      "keyword": "关键词",
      "name": "规则名称",
      "reply": "回复内容",
      "enabled": true
    }
  ]
}
```

### 监控控制

```bash
# 启动监控
POST /api/start

# 停止监控
POST /api/stop

# 获取状态
GET /api/status

# 获取日志
GET /api/logs

# 清空日志
DELETE /api/logs
```

### 其他API

```bash
# 导出配置
GET /api/export-config

# 导入配置
POST /api/import-config

# 验证配置文件
POST /api/validate-config-file
```

## ❓ 常见问题

### Q: 如何获取 SESSDATA 和 bili_jct？

A: 在浏览器中访问 https://message.bilibili.com/，按 F12 打开开发者工具，切换到 Network 标签，刷新页面，在请求头中找到 Cookie，复制相应的值。

### Q: 为什么AI回复质量不好？

A:
1. 检查RAG服务是否正常运行
2. 确保发送给RAG服务的提示词清晰
3. 调整系统提示词以获得更好的效果
4. 确保RAG服务的文档库包含相关信息

### Q: 支持哪些AI服务？

A: 目前支持：
- Claude (Anthropic API) - 通过ai_adapter.py集成
- 智谱 GLM 系列 - 原有AI Agent支持
- 自定义RAG服务 - 通过RAG适配器

### Q: 系统占用多少内存？

A: 基础运行约100-200MB，消息缓存会根据负载增长，有自动清理机制。

### Q: 如何处理频率限制？

A:
1. 增加 `send_delay_interval` (发送间隔)
2. 增加 `message_check_interval` (检查间隔)
3. 增加 `follow_check_interval` (关注者检查间隔)

### Q: 可以同时运行多个实例吗？

A: 不建议，容易触发B站风控。建议使用单实例 + 异步处理。

## 🔧 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| Web框架 | Flask | 提供Web UI和REST API |
| AI模型 | Claude 3.5 Sonnet | 智能回复 |
| RAG服务 | 自定义 | 检索增强生成 |
| B站API | HTTP REST | 获取和发送私信 |
| 存储 | JSON文件 | 配置和规则持久化 |
| 前端 | HTML/CSS/JS | Web管理界面 |

## 📝 日志说明

- **[SUCCESS]**: 操作成功
- **[INFO]**: 普通信息
- **[WARNING]**: 警告信息
- **[ERROR]**: 错误信息
- **[DEBUG]**: 调试信息

日志实时显示在Web界面，支持按级别筛选和导出。

## 🐛 已知问题

1. **AI响应过长**: 某些情况下AI生成的回复可能超过B站字数限制，需要在RAG服务端进行长度控制
2. **频率限制**: B站API有频率限制，需要合理调整各项间隔参数
3. **对话历史**: 长期运行时对话缓存可能占用较多内存，已实现自动清理机制

## 📖 开发指南

### 项目结构

```
BiliGo/
├── app.py                      # Flask应用主文件
├── ai_adapter.py               # AI适配器（RAG服务集成）
├── send_ai_reply.py            # 单条消息回复脚本
├── test_ai_adapter.py          # AI适配器测试
├── test_bilibili_integration.py # 集成测试
├── config.json                 # 配置文件
├── config.json.sample          # 配置示例
├── keywords.json               # 规则配置
├── requirements.txt            # Python依赖
├── index.html                  # Web主页
├── logs.html                   # 日志页面
├── README.md                   # 本文件
└── ENV_SETUP.md               # 环境配置指南
```

### 模块说明

- **BilibiliAPI**: B站API接口封装
- **AIReplyAdapter**: AI回复适配器，支持多种后端
- **monitor_messages()**: 主监控循环，处理私信
- **check_keywords_fast()**: 关键词快速匹配

### 运行测试

```bash
# 运行所有测试
python -m pytest

# 运行特定测试
python -m pytest test_ai_adapter.py -v

# 测试覆盖率
python -m pytest --cov=.
```

## 🔐 安全建议

1. **不要硬编码敏感信息**: 使用环境变量存储凭证
2. **定期更新**: 及时获取最新的SESSDATA和bili_jct
3. **监控日志**: 定期检查异常日志
4. **限制访问**: Web界面建议在内网使用或使用反向代理保护
5. **备份配置**: 定期备份rules和config

## 📞 致谢与反馈

### 原项目作者

本项目基于原BiliGo项目，感谢原作者的贡献！

- **UP主B站主页**: https://space.bilibili.com/404891612
- **UP主QQ**: 3083248889

### 当前维护者

- **当前维护者B站主页**: https://space.bilibili.com/372287303
- 负责RAG服务集成、AI适配器、现代化重构等工作

### 贡献

欢迎提交Issue和Pull Request！

### 问题反馈

有任何问题欢迎反馈：

- GitHub Issues: https://github.com/Wu-ChengLiang/BiliGo/issues
- B站私信: https://space.bilibili.com/372287303
- 或通过Issue标签联系

## 📄 许可证

本项目遵循原项目的许可证要求，继承自BiliGo原项目。

---

**最后更新**: 2025-10-31
**版本**: 2.0 (AI Agent + RAG Service Integration)
