# Claude Local Agent CLI
A local-executable AI Agent command-line tool built on the Claude Agent SDK, with native `superpowers` skill pack integration, real-time execution feedback, and one-click packaging & distribution capabilities.

---

## 📋 Features
- 🔒 **Data Security & Privacy**: All tool calls and code operations run locally on your device, only task prompts and AI thinking flow are sent to the Claude API
- 🛠️ **Extensible Skills**: Native integration with the `superpowers` skill pack, with full support for custom skill development
- 💬 **Real-time Feedback**: Full lifecycle status prompts, including AI thinking flow, tool call details, heartbeat prompts for long-running tasks
- ⏱️ **Execution Metrics**: Auto-calculated and displayed task execution time
- 📦 **Portable Packaging**: Support for packaging into standalone executable files, no Python/Claude SDK installation required on target devices
- 🚀 **Lightweight & Fast**: Minimal dependencies, quick startup, and low resource consumption

---

## 📦 Prerequisites
| Dependency | Version Requirement | Description |
|------------|----------------------|-------------|
| Python     | 3.10 ~ 3.12          | Core runtime environment |
| Node.js    | 20+                  | Runtime for the `superpowers` skill pack |
| Git        | Latest               | For code version management and repository cloning |
| Homebrew   | Latest               | macOS package manager (for installing Python/Node.js) |

---

## 🚀 Quick Start
### 1. Clone the Repository
```bash
git clone https://github.com/Haven-1999/claude-local-agent.git
cd claude-local-agent
```

### 2. Install Python Dependencies
```bash
# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy the example environment file and fill in your configuration:
```bash
cp .env.example .env
```

`.env` configuration template:
```env
# Third-party Claude API Configuration
ANTHROPIC_API_KEY=your-api-key-here
ANTHROPIC_BASE_URL=https://your-proxy-url/v1
MODEL_NAME=claude-3-5-sonnet-20241022
```

### 4. Prepare the `superpowers` Skill Pack
```bash
# Clone the superpowers repository
git clone https://github.com/your-org/superpowers.git ./superpowers

# Install dependencies for superpowers (if required)
cd superpowers
npm install
cd ..
```

### 5. Run the Project
```bash
python claude_service.py "List files in the current directory"
```

---

## 📖 Usage Guide
### Basic Usage
```bash
python claude_service.py "your task description here"
```

### Call Skills
Use the `/skill-skill-name` format to call `superpowers` skills:
```bash
# Call a single skill
python claude_service.py "Brainstorm an AI project idea /skill-brainstorming"

# Call multiple skills
python claude_service.py "Write test cases and refactor code /skill-test-driven-development /skill-refactor"
```

---

## 📦 Packaging & Distribution (macOS Only)
Package the project into a standalone executable file for distribution to other macOS devices.

### 1. Prepare Packaging Environment
Ensure your virtual environment is activated, and the `superpowers` folder is in the project root directory:
```bash
source .venv/bin/activate
ls -la superpowers  # Verify the folder exists
```

### 2. Run Packaging Command
```bash
# Install PyInstaller
pip install pyinstaller

# One-click packaging (includes main program, superpowers, and .env template)
pyinstaller -F \
  --add-data "./superpowers:superpowers" \
  --add-data ".env:." \
  claude_service.py
```

### 3. Deliverable Files
After packaging is complete, distribute the following files/folders together:
```
dist/claude_service  # Main executable (in the dist directory)
.env                  # Environment configuration file (to be provided separately, protect your API Key)
superpowers/          # Full superpowers folder
```

### 4. Run on Target Device
1.  Place all delivered files in the same directory on the target device
2.  Ensure Node.js is installed on the target device (verify with `node --version`)
3.  Run the following commands in terminal:
    ```bash
    # Grant execution permission
    chmod +x claude_service

    # Remove macOS quarantine attribute (if "cannot be opened" error occurs)
    xattr -c claude_service

    # Run the program
    ./claude_service "your task /skill-skill-name"
    ```

---

## ❓ FAQ
### Q: `command not found: node` error when running
**A**: Node.js is not installed on the target device. Please download and install it from [nodejs.org](https://nodejs.org/).

### Q: macOS error "cannot be opened because the developer cannot be verified"
**A**: Run `xattr -c claude_service` to remove the quarantine attribute, or allow execution in **System Settings → Privacy & Security**.

### Q: 403 Permission Denied when pushing to GitHub
**A**: GitHub no longer supports password authentication for HTTPS pushes. You must use a **Personal Access Token (PAT)** with the `repo` scope enabled as your password.

### Q: No token consumption statistics displayed
**A**: Token statistics are not implemented in this project due to SDK limitations. For accurate usage metrics, please check your third-party API proxy console.

---

## 🤝 Contributing
Contributions, issues, and pull requests are welcome!
1.  Fork this repository
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
