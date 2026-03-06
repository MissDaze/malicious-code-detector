# 🛡️ Malicious Code Detector

AI-powered malicious code detection agent that analyzes source code for security vulnerabilities, malicious patterns, and suspicious behavior.

## Features

- 🤖 **AI-Powered Analysis** - Uses CodeLlama via Ollama for intelligent code review
- 🔍 **Pattern Matching** - Detects known malicious code signatures
- ⚡ **Static Analysis** - Identifies suspicious code patterns
- 🌐 **REST API** - Easy integration with your workflow
- 🆓 **100% Free** - Uses open-source models, no API costs

## Detects

- **Backdoors** - Hidden remote access mechanisms
- **Data Exfiltration** - Unauthorized data transmission
- **Code Injection** - SQL injection, command injection, XSS
- **Obfuscation** - Deliberately obscured malicious code
- **Cryptominers** - Hidden cryptocurrency mining code
- **Privilege Escalation** - Attempts to gain unauthorized access
- **Suspicious System Calls** - Dangerous OS operations

## Installation

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai) installed locally

### Setup

1. Clone the repository:
```bash
git clone https://github.com/MissDaze/malicious-code-detector.git
cd malicious-code-detector
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Pull the AI model:
```bash
ollama pull codellama:7b
```

4. Start the detection agent:
```bash
python agent.py
```

## Usage

### Web Interface
Open `http://localhost:5000` in your browser and paste code to analyze.

### API

**Analyze code:**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "your code here", "language": "python"}'
```

**Response:**
```json
{
  "risk_level": "high",
  "score": 85,
  "threats": [
    {
      "type": "command_injection",
      "severity": "critical",
      "line": 12,
      "description": "Unsafe use of os.system() with user input",
      "recommendation": "Use subprocess with shell=False"
    }
  ],
  "ai_analysis": "This code contains patterns typical of remote access trojans..."
}
```

### Python SDK

```python
from detector import MaliciousCodeDetector

detector = MaliciousCodeDetector()
result = detector.analyze(code, language="python")

if result.risk_level == "high":
    print(f"⚠️ Threats found: {result.threats}")
```

### CLI

```bash
# Analyze a file
python cli.py analyze --file suspicious.py

# Analyze a directory
python cli.py scan --dir ./project

# Watch mode (continuous monitoring)
python cli.py watch --dir ./src
```

## Configuration

Edit `config.yaml`:

```yaml
ai_model: codellama:7b  # Ollama model to use
threshold: 60           # Risk score threshold (0-100)
enable_ai: true         # Use AI analysis (slower but more accurate)
enable_patterns: true   # Use pattern matching (fast)
languages:
  - python
  - javascript
  - php
  - bash
```

## How It Works

1. **Pattern Matching** - Fast initial scan using regex patterns for known malicious code
2. **Static Analysis** - AST parsing to detect suspicious structures
3. **AI Analysis** - CodeLlama analyzes code semantics and context
4. **Risk Scoring** - Combines all signals into a 0-100 risk score

## Examples

See `examples/` for sample malicious code patterns the agent can detect.

## Contributing

PRs welcome! Add new detection patterns in `patterns/` directory.

## License

MIT License - See LICENSE file

## Disclaimer

This tool is for security research and defensive purposes only. The maintainers are not responsible for misuse.
