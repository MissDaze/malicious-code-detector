# Quick Start Guide

Get up and running in 5 minutes!

## Option 1: Without AI (Fastest - No Setup Required)

If you don't want to install Ollama, you can use pattern matching only:

1. **Install Python dependencies:**
```bash
pip install flask flask-cors pyyaml requests colorama click
```

2. **Disable AI in config.yaml:**
```yaml
enable_ai: false
```

3. **Run the agent:**
```bash
python agent.py
```

4. **Open http://localhost:5000** and start analyzing!

## Option 2: With AI (Most Accurate)

For full AI-powered analysis:

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Install Ollama:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

3. **Download AI model:**
```bash
ollama pull codellama:7b
```
*(This is a 4GB download - wait for completion)*

4. **Start Ollama (if not running):**
```bash
ollama serve &
```

5. **Start the agent:**
```bash
python agent.py
```

6. **Open http://localhost:5000**

## Quick Test

Run the test suite to verify everything works:

```bash
python test.py
```

You should see:
- ✅ Backdoor code detected (HIGH risk)
- ✅ Safe code passes (LOW risk)
- ✅ PHP injection detected (CRITICAL risk)

## Usage Examples

### Web Interface
1. Paste code in the text box
2. Select language
3. Click "Analyze Code"
4. View threats and AI analysis

### CLI - Analyze a file
```bash
python cli.py analyze --file suspicious.py
```

### CLI - Scan a directory
```bash
python cli.py scan --dir ./myproject
```

### CLI - Watch mode (continuous)
```bash
python cli.py watch --dir ./src --interval 5
```

### API
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "import os\nos.system(user_input)",
    "language": "python"
  }'
```

## Test with Examples

The `examples/` folder contains sample malicious code:

```bash
# Test backdoor detection
python cli.py analyze --file examples/backdoor.py

# Test data exfiltration detection
python cli.py analyze --file examples/data_exfil.py

# Test safe code (should be clean)
python cli.py analyze --file examples/safe_code.py

# Scan all examples
python cli.py scan --dir examples
```

## Configuration

Edit `config.yaml` to customize:

- `threshold`: Risk score threshold (0-100)
- `ai_model`: Which Ollama model to use
- `enable_ai`: Turn AI analysis on/off
- `server.port`: Change web interface port

## Troubleshooting

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**"Connection refused" (Ollama)**
```bash
ollama serve &
```

**Port 5000 already in use**
Edit `config.yaml` and change the port to 8080 or another free port.

## Next Steps

- Add custom detection patterns in `detector.py`
- Integrate with CI/CD pipeline via API
- Use CLI in git pre-commit hooks
- Schedule periodic scans with cron

## Need Help?

- 📚 Full docs: See README.md
- 🐛 Issues: https://github.com/MissDaze/malicious-code-detector/issues
- 💬 Discussions: https://github.com/MissDaze/malicious-code-detector/discussions

Happy hunting! 🛡️
