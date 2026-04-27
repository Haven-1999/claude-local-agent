# Claude Agent SDK 本地部署与打包指南
基于 Claude Agent SDK 构建的本地 AI Agent，集成 `superpowers` 技能包，支持命令行交互、实时反馈与跨设备打包分发。

---

## 📋 功能特性
- 🔒 **数据安全**：所有工具调用本地执行，仅任务描述与 AI 思考经过 Claude API
- 🛠️ **技能扩展**：原生集成 `superpowers` 技能包，支持自定义技能开发
- 💬 **实时反馈**：提供思考过程、工具调用、心跳提示等全流程状态
- ⏱️ **耗时统计**：自动记录任务执行耗时
- 📦 **可打包分发**：支持打包为独立可执行文件，目标设备无需安装 Python/Claude SDK

---

## 📦 前置要求
| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Python | 3.10 ~ 3.12 | 核心运行环境 |
| Node.js | 20+ | `superpowers` 技能包运行环境 |
| Homebrew | 最新版 | macOS 包管理器（用于安装 Python/Node.js） |
| Git | 最新版 | 代码版本管理 |

---

## 🚀 快速开始
### 1. 克隆仓库
```bash
git clone <your-repo-url>
cd claude-agent-mac
```

### 2. 安装 Python 依赖
```bash
# 创建虚拟环境
python3.11 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量
复制 `.env.example` 为 `.env` 并填入你的配置：
```bash
cp .env.example .env
open .env
```

`.env` 配置示例：
```env
# 第三方 Claude 配置
ANTHROPIC_API_KEY=your-api-key-here
ANTHROPIC_BASE_URL=https://your-proxy-url/v1
MODEL_NAME=claude-3-5-sonnet-20241022
```

### 4. 准备 `superpowers` 技能包
```bash
# 克隆 superpowers 仓库到 skills 目录
git clone https://github.com/your-org/superpowers.git ./superpowers

# 安装 superpowers 依赖（如果需要）
cd superpowers
npm install
cd ..
```

### 5. 运行项目
```bash
python claude_service.py "查看当前目录文件"
```

---

## 📖 使用指南
### 基础使用
```bash
python claude_service.py "你的任务描述"
```

### 调用技能
使用 `/skill-技能名` 格式调用 `superpowers` 技能：
```bash
# 调用单个技能
python claude_service.py "帮我头脑风暴一个 AI 项目 /skill-brainstorming"

# 调用多个技能
python claude_service.py "写测试用例并重构代码 /skill-test-driven-development /skill-refactor"
```

---

## 📦 打包分发（macOS 专属）
### 1. 准备打包环境
确保虚拟环境已激活，且 `superpowers` 文件夹在项目根目录：
```bash
source .venv/bin/activate
ls -la superpowers  # 确认文件夹存在
```

### 2. 执行打包
```bash
# 安装 PyInstaller
pip install pyinstaller

# 一键打包（包含主程序、superpowers、.env）
pyinstaller -F \
  --add-data "./superpowers:superpowers" \
  --add-data ".env:." \
  claude_service.py
```

### 3. 交付文件
打包完成后，将以下文件/文件夹一起分发：
```
dist/claude_service  # 主程序（在 dist 目录）
.env                  # 配置文件（需单独提供，保护 API Key）
superpowers/          # 整个 superpowers 文件夹
```

### 4. 目标设备运行
1. 将所有文件放在同一目录
2. 确保目标设备已安装 Node.js（`node --version` 验证）
3. 执行以下命令：
   ```bash
   # 赋予执行权限
   chmod +x claude_service
   
   # 移除 macOS 隔离属性（如遇“无法打开”报错）
   xattr -c claude_service
   
   # 运行
   ./claude_service "你的任务 /skill-技能名"
   ```

---

## ❓ 常见问题
### Q: 报错 `command not found: node`
**A**: 目标设备未安装 Node.js，请前往 [nodejs.org](https://nodejs.org/) 下载安装。

### Q:  macOS 报错“无法打开，因为无法验证开发者”
**A**: 执行 `xattr -c claude_service` 移除隔离属性，或在“系统设置 → 隐私与安全性”中允许运行。

### Q: Token 统计显示为 0
**A**: 因 SDK 限制，本项目未实现 Token 统计，精确消耗请查看第三方代理服务控制台。

---

## 🤝 贡献指南
欢迎提交 Issue 和 Pull Request！
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证
本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。
