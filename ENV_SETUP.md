# BiliGo 环境变量配置指南

本项目采用环境变量管理敏感凭证，确保不在代码库中暴露密钥和登录信息。

## 必需环境变量

### B站登录凭证
```bash
# B站 SESSDATA（从浏览器 Cookie 获取）
export BILI_SESSDATA="your_sessdata_here"

# B站 CSRF 令牌（从浏览器 Cookie 获取）
export BILI_JCT="your_bili_jct_here"
```

### AI 服务凭证
```bash
# 智谱 (ZhipuAI) API 密钥（可选，仅在使用 AI Agent 时需要）
export ZHIPU_API_KEY="your_zhipu_api_key_here"

# Anthropic Claude API 密钥（可选，预留给未来使用）
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"
```

### 可选环境变量
```bash
# RAG 服务地址（默认：http://127.0.0.1:8000）
export RAG_SERVICE_URL="http://127.0.0.1:8000"
```

## 设置方法

### 方法1：通过 .env 文件（推荐）

1. 在项目根目录创建 `.env` 文件：
```
BILI_SESSDATA=your_sessdata_here
BILI_JCT=your_bili_jct_here
ZHIPU_API_KEY=your_zhipu_api_key_here
RAG_SERVICE_URL=http://127.0.0.1:8000
```

2. 安装 python-dotenv（如果未安装）：
```bash
pip install python-dotenv
```

3. 在应用启动时加载 .env 文件（在 `app.py` 顶部添加）：
```python
from dotenv import load_dotenv
load_dotenv()
```

### 方法2：通过系统环境变量

**Linux/Mac：**
```bash
# 临时设置（仅当前会话有效）
export BILI_SESSDATA="..."
export BILI_JCT="..."

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export BILI_SESSDATA="..."' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell)：**
```powershell
$env:BILI_SESSDATA="..."
$env:BILI_JCT="..."

# 永久设置：通过控制面板 → 系统 → 高级系统设置 → 环境变量
```

### 方法3：Docker/容器部署
```bash
docker run -e BILI_SESSDATA="..." -e BILI_JCT="..." your_image
```

## 如何获取凭证

### 获取 BILI_SESSDATA 和 BILI_JCT

1. 打开浏览器，访问 https://www.bilibili.com
2. 登录您的 B站 账号
3. 打开开发者工具（F12）→ 应用程序 → Cookie
4. 搜索并复制：
   - `SESSDATA` → 设置为 `BILI_SESSDATA`
   - `bili_jct` → 设置为 `BILI_JCT`

### 获取 ZHIPU_API_KEY

1. 访问 https://open.bigmodel.cn/
2. 注册/登录智谱账号
3. 创建 API 密钥
4. 复制密钥值

## 凭证管理最佳实践

✅ **应该做**：
- 所有敏感凭证都通过环境变量传入
- 使用 `.env` 文件在本地开发（添加到 .gitignore）
- 在生产环境使用系统环境变量或密钥管理服务
- 定期轮换登录凭证
- 使用专用的 B站 账号而非个人账号

❌ **不应该做**：
- 将凭证硬编码在源代码中
- 将 `config.json` 包含真实凭证提交到版本控制
- 在日志中输出敏感信息
- 在不安全的渠道传输凭证

## 验证环境变量

启动应用时会在日志中显示：
```
[INFO] 从环境变量 BILI_SESSDATA 加载成功
[INFO] 从环境变量 BILI_JCT 加载成功
[INFO] 从环境变量 ZHIPU_API_KEY 加载成功
```

如果看不到这些日志，说明环境变量未正确设置。

## 配置优先级

应用会按以下优先级加载配置：

1. **环境变量**（最高优先级）- 覆盖 config.json
2. **config.json** - 本地配置文件
3. **默认值** - 代码中的硬编码默认值

这意味着环境变量会优先使用，提高安全性。

## 故障排查

**问题1：环境变量未被加载**
```bash
# 检查环境变量是否设置
echo $BILI_SESSDATA
echo $BILI_JCT

# 如果为空，重新设置环境变量
```

**问题2：登录状态失效错误**
- BILI_SESSDATA 或 BILI_JCT 可能已过期
- 需要重新从浏览器 Cookie 中获取并更新环境变量

**问题3：AI 相关错误**
- 检查 ZHIPU_API_KEY 是否正确设置
- 检查 RAG 服务是否运行（默认 http://127.0.0.1:8000）
