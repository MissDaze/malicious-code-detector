# 🛡️ Malicious Code Detector - Project Summary

## 🎯 Project Overview

An AI-powered security tool that analyzes source code for malicious patterns, vulnerabilities, and suspicious behavior. Built with free/open-source technologies.

**Repository:** https://github.com/MissDaze/malicious-code-detector

## 🚀 Key Features

### 1. **AI-Powered Analysis**
- Uses CodeLlama (7B parameter model) via Ollama
- Semantic understanding of code intent
- Contextual threat detection
- 100% free - runs locally

### 2. **Pattern Matching Engine**
- 40+ malicious code patterns
- Language-specific detection rules
- Fast initial scanning
- Known vulnerability signatures

### 3. **Static Code Analysis**
- AST (Abstract Syntax Tree) parsing
- Dataflow analysis
- Suspicious function detection
- Import/dependency checking

### 4. **Multi-Language Support**
- Python
- JavaScript/TypeScript
- PHP
- Bash/Shell
- Ruby, Java, C/C++

## 🛠️ Technical Architecture

```
┌─────────────────────────────────────────┐
│         Web Interface / CLI             │
│        (Flask + HTML/JavaScript)        │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         Detection Engine                │
│         (detector.py)                   │
├─────────────────────────────────────────┤
│  1. Pattern Matching (regex)            │
│  2. Static Analysis (AST)               │
│  3. AI Analysis (Ollama)                │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         Risk Scoring                    │
│   (Critical/High/Medium/Low)            │
└─────────────────────────────────────────┘
```

## 📦 What's Included

### Core Files
- `agent.py` - Web server and API
- `detector.py` - Detection engine
- `cli.py` - Command-line interface
- `config.yaml` - Configuration
- `requirements.txt` - Python dependencies

### Documentation
- `README.md` - Full documentation
- `QUICKSTART.md` - 5-minute setup guide
- `INSTALL.md` - Detailed installation
- `LICENSE` - MIT license

### Examples
- `examples/backdoor.py` - Reverse shell example
- `examples/data_exfil.py` - Data exfiltration
- `examples/code_injection.php` - PHP vulnerabilities
- `examples/safe_code.py` - Clean code sample

### Testing
- `test.py` - Automated test suite

## 🎯 Detection Capabilities

### Critical Threats
- ✅ Remote code execution
- ✅ Backdoors and reverse shells
- ✅ Command injection
- ✅ Code injection (eval/exec)
- ✅ Unsafe deserialization

### High-Risk Patterns
- ✅ Data exfiltration
- ✅ SQL injection
- ✅ XSS vulnerabilities
- ✅ Unsafe system calls
- ✅ Dangerous file operations

### Medium-Risk Indicators
- ✅ Network communication
- ✅ Code obfuscation
- ✅ Suspicious imports
- ✅ Input validation issues
- ✅ Cryptographic operations

## 📊 Performance

- **Pattern Matching:** <100ms per file
- **Static Analysis:** 200-500ms per file
- **AI Analysis:** 2-5 seconds per file
- **Memory Usage:** ~500MB (with AI model loaded)

## 🌐 Use Cases

### 1. **Development Security**
Scan code during development to catch vulnerabilities early

### 2. **Code Review**
Automated first-pass security review before human review

### 3. **CI/CD Integration**
Block deployments containing malicious patterns

### 4. **Security Audits**
Scan entire codebases for security issues

### 5. **Educational Tool**
Learn about malicious code patterns and security

### 6. **Incident Response**
Quickly analyze suspicious scripts found on systems

## 🔧 Integration Options

### API Integration
```python
import requests

response = requests.post('http://localhost:5000/api/analyze', json={
    'code': suspicious_code,
    'language': 'python'
})

result = response.json()
if result['risk_level'] in ['high', 'critical']:
    alert_security_team(result)
```

### Git Pre-commit Hook
```bash
#!/bin/bash
python cli.py analyze --file "$1" --threshold 60
```

### GitHub Actions
```yaml
- name: Scan for malicious code
  run: |
    pip install -r requirements.txt
    python cli.py scan --dir . --recursive
```

## 🎓 Educational Value

The project includes:
- Real malicious code examples (safe to run in isolated environment)
- Comments explaining why each pattern is dangerous
- Recommended fixes for each vulnerability type
- Security best practices

## 🔮 Future Enhancements

Potential additions:
- [ ] More language support (Go, Rust, Swift)
- [ ] Browser extension for GitHub/GitLab
- [ ] VS Code plugin for real-time detection
- [ ] Machine learning model training on custom datasets
- [ ] Integration with vulnerability databases (CVE, NVD)
- [ ] Automated fix suggestions
- [ ] Compliance checking (OWASP, CWE)
- [ ] Docker/container scanning

## 📈 Success Metrics

Test results on example files:
- **Backdoor detection:** 65/100 (HIGH) ✅
- **Data exfiltration:** Detected ✅
- **Code injection (PHP):** 100/100 (CRITICAL) ✅
- **Safe code:** 0/100 (CLEAN) ✅

**False positive rate:** Low (clean code scores 0)

## 🤝 Contributing

The codebase is well-structured for contributions:
- Add new patterns in `detector.py` `_load_patterns()`
- Extend static analysis in `_static_analysis_python()`
- Add language support by creating new pattern sets
- Improve AI prompts in `_ai_analyze()`

## 💡 Why This Project Matters

1. **Democratizes Security:** Free tools for everyone
2. **Educational:** Learn by doing
3. **Practical:** Solves real problems
4. **Privacy-First:** All analysis runs locally
5. **Open Source:** Transparent and auditable

## 🎉 Getting Started

**Fastest way to try it:**
```bash
git clone https://github.com/MissDaze/malicious-code-detector.git
cd malicious-code-detector
pip install flask pyyaml requests
python agent.py
# Open http://localhost:5000
```

**Full setup with AI:**
See QUICKSTART.md

## 📞 Support

- GitHub Issues: Report bugs
- GitHub Discussions: Ask questions
- Pull Requests: Contribute improvements

---

**Built with ❤️ for the security community**
