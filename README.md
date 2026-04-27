# Claude Local Agent CLI
A lightweight, local AI Agent CLI built with **Claude Agent SDK**.  
**Auto-discovers & loads all skills** from the `skills/` directory — zero code changes required.

---

## Features
- 🔒 **Privacy-Focused**: All tool execution runs locally; only prompts go to the API
- 📂 **Unified Skill Directory**: Drop any open-source skill into `skills/` and auto-load
- 🛠️ **Multi-Skill Support**: Automatically scans and loads all subfolders in `skills/`
- 💬 **Real-time Feedback**: AI thinking, tool calls, and progress display
- ⏱️ **Execution Timer**: Automatically shows time elapsed
- 📦 **One-Command Build**: Package to standalone macOS executable
- 🚀 **Zero-Config Setup**: No manual path configuration

---

## Project Structure
```
claude-local-agent/
├── skills/             # All skills go here (auto-scanned)
│   ├── superpowers/    # Example official skill
│   └── your-skill/     # Add any new skill here
├── claude_service.py   # Main agent (auto-loads skills)
├── .env.example        # Env template
├── requirements.txt    # Python dependencies
└── .gitignore
```

---

## Prerequisites
- Python 3.10 ~ 3.12
- Node.js 20+ (for skill plugins)
- Git

---

## Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/Haven-1999/claude-local-agent.git
cd claude-local-agent
```

### 2. Set up Python environment
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
```

Edit `.env`:
```env
ANTHROPIC_API_KEY=your-api-key
ANTHROPIC_BASE_URL=https://your-proxy-url/v1
MODEL_NAME=claude-3-5-sonnet-20241022
```

### 4. Install Skills (Auto-Loaded)
All skills go into the `skills/` directory.

```bash
mkdir -p skills

# Install superpowers (example)
git clone https://github.com/anthropics/superpowers.git skills/superpowers
cd skills/superpowers
npm install
cd ../..
```

### 5. Run the agent
```bash
python claude_service.py "List current directory files"
```

You will see:
```
[Agent] Auto-loaded skill: superpowers
```

---

## Usage

### Basic task
```bash
python claude_service.py "Your task description"
```

### Call a skill
```bash
python claude_service.py "Brainstorm a project /skill-brainstorming"
```

### Multiple skills
```bash
python claude_service.py "Write tests and refactor /skill-test-driven-development /skill-refactor"
```

---

## How to Add New Skills
1. Create a folder inside `skills/`
2. Place your skill files inside
3. Restart the agent — it will **auto-load**

No code changes needed.

---

## Build Standalone Binary (macOS)
Package the agent + all skills into a single executable.

### 1. Clean old builds
```bash
rm -rf build dist *.spec
```

### 2. Build
```bash
pip install pyinstaller

pyinstaller -F \
  --add-data "./skills:skills" \
  --add-data ".env:." \
  claude_service.py
```

### 3. Output
```
dist/claude_service
```

---

## Distribute to Another Mac
Send these 3 items:
```
dist/claude_service
.env
skills/
```

### Run on target machine
```bash
chmod +x claude_service
xattr -c claude_service
./claude_service "Your task /skill-brainstorming"
```

---

## FAQ

### Q: Where to install skills?
A: All skills go into the `skills/` directory.

### Q: How are skills loaded?
A: The agent **automatically scans and loads all subfolders** in `skills/` at startup.

### Q: Missing `node` command?
A: Install Node.js from [nodejs.org](https://nodejs.org).

### Q: macOS “cannot verify developer”?
A: Run `xattr -c claude_service`

---

## License
MIT License
