#!/usr/bin/env python3
"""
Quick test script for the malicious code detector
"""

from detector import MaliciousCodeDetector
import yaml

# Load config
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Disable AI for quick testing
config['enable_ai'] = False

detector = MaliciousCodeDetector(config)

print("🛡️  Testing Malicious Code Detector\n")

# Test 1: Malicious code
print("Test 1: Analyzing backdoor.py (should detect threats)")
print("-" * 60)
with open('examples/backdoor.py', 'r') as f:
    code = f.read()

result = detector.analyze(code, 'python')
print(f"Risk Level: {result['risk_level'].upper()}")
print(f"Score: {result['score']}/100")
print(f"Threats found: {len(result['threats'])}")
for threat in result['threats'][:3]:
    print(f"  • {threat['type']}: {threat['description']}")
print()

# Test 2: Safe code
print("Test 2: Analyzing safe_code.py (should be clean)")
print("-" * 60)
with open('examples/safe_code.py', 'r') as f:
    code = f.read()

result = detector.analyze(code, 'python')
print(f"Risk Level: {result['risk_level'].upper()}")
print(f"Score: {result['score']}/100")
print(f"Threats found: {len(result['threats'])}")
print()

# Test 3: PHP injection
print("Test 3: Analyzing code_injection.php (should detect critical issues)")
print("-" * 60)
with open('examples/code_injection.php', 'r') as f:
    code = f.read()

result = detector.analyze(code, 'php')
print(f"Risk Level: {result['risk_level'].upper()}")
print(f"Score: {result['score']}/100")
print(f"Threats found: {len(result['threats'])}")
for threat in result['threats'][:5]:
    print(f"  • {threat['type']}: {threat['description']}")
print()

print("✅ All tests complete!")
