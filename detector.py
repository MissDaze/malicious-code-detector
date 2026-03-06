"""
Core detection engine combining AI analysis, pattern matching, and static analysis
"""

import re
import ast
import requests
from typing import Dict, List, Any
import json

class MaliciousCodeDetector:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.patterns = self._load_patterns()
        
    def _load_patterns(self) -> Dict[str, List[Dict]]:
        """Load malicious code patterns"""
        return {
            'python': [
                {
                    'pattern': r'os\.system\([^)]*\)',
                    'type': 'command_injection',
                    'severity': 'high',
                    'description': 'Unsafe use of os.system() - potential command injection',
                    'recommendation': 'Use subprocess.run() with shell=False'
                },
                {
                    'pattern': r'eval\([^)]*\)',
                    'type': 'code_injection',
                    'severity': 'critical',
                    'description': 'Use of eval() with untrusted input',
                    'recommendation': 'Avoid eval() or use ast.literal_eval() for safe parsing'
                },
                {
                    'pattern': r'exec\([^)]*\)',
                    'type': 'code_injection',
                    'severity': 'critical',
                    'description': 'Use of exec() - can execute arbitrary code',
                    'recommendation': 'Remove exec() or strictly validate input'
                },
                {
                    'pattern': r'__import__\([\'"]os[\'"]\)',
                    'type': 'suspicious_import',
                    'severity': 'medium',
                    'description': 'Dynamic import of os module',
                    'recommendation': 'Use standard imports'
                },
                {
                    'pattern': r'pickle\.loads?\(',
                    'type': 'deserialization',
                    'severity': 'high',
                    'description': 'Unsafe deserialization with pickle',
                    'recommendation': 'Use json or validate pickle source'
                },
                {
                    'pattern': r'socket\.socket\(',
                    'type': 'network_communication',
                    'severity': 'medium',
                    'description': 'Creates network socket - potential backdoor',
                    'recommendation': 'Review network communication necessity'
                },
                {
                    'pattern': r'subprocess\..*shell\s*=\s*True',
                    'type': 'command_injection',
                    'severity': 'high',
                    'description': 'subprocess with shell=True is vulnerable to injection',
                    'recommendation': 'Use shell=False and pass command as list'
                },
                {
                    'pattern': r'base64\.b64decode',
                    'type': 'obfuscation',
                    'severity': 'medium',
                    'description': 'Base64 decoding often used to hide malicious code',
                    'recommendation': 'Verify decoded content'
                },
                {
                    'pattern': r'requests\.(get|post)\([^)]*\)',
                    'type': 'data_exfiltration',
                    'severity': 'medium',
                    'description': 'HTTP request - potential data exfiltration',
                    'recommendation': 'Review destination and data being sent'
                },
                {
                    'pattern': r'cryptography|hashlib|Crypto',
                    'type': 'crypto_operations',
                    'severity': 'low',
                    'description': 'Cryptographic operations - could be ransomware',
                    'recommendation': 'Verify legitimate use'
                }
            ],
            'javascript': [
                {
                    'pattern': r'eval\(',
                    'type': 'code_injection',
                    'severity': 'critical',
                    'description': 'eval() executes arbitrary JavaScript',
                    'recommendation': 'Remove eval() or use Function constructor carefully'
                },
                {
                    'pattern': r'document\.write\(',
                    'type': 'xss',
                    'severity': 'high',
                    'description': 'document.write() can inject malicious HTML',
                    'recommendation': 'Use DOM manipulation methods instead'
                },
                {
                    'pattern': r'innerHTML\s*=',
                    'type': 'xss',
                    'severity': 'high',
                    'description': 'innerHTML assignment can lead to XSS',
                    'recommendation': 'Use textContent or sanitize input'
                },
                {
                    'pattern': r'XMLHttpRequest|fetch\(',
                    'type': 'data_exfiltration',
                    'severity': 'medium',
                    'description': 'HTTP request to external server',
                    'recommendation': 'Verify destination URL'
                },
                {
                    'pattern': r'atob\(|btoa\(',
                    'type': 'obfuscation',
                    'severity': 'medium',
                    'description': 'Base64 encoding/decoding',
                    'recommendation': 'Check decoded content'
                },
                {
                    'pattern': r'window\.location\s*=',
                    'type': 'redirection',
                    'severity': 'medium',
                    'description': 'Forced redirection to external site',
                    'recommendation': 'Validate destination'
                }
            ],
            'php': [
                {
                    'pattern': r'eval\(',
                    'type': 'code_injection',
                    'severity': 'critical',
                    'description': 'eval() executes arbitrary PHP code',
                    'recommendation': 'Remove eval() completely'
                },
                {
                    'pattern': r'system\(|exec\(|shell_exec\(|passthru\(',
                    'type': 'command_injection',
                    'severity': 'critical',
                    'description': 'Executes system commands',
                    'recommendation': 'Avoid or use escapeshellcmd()'
                },
                {
                    'pattern': r'\$_(GET|POST|REQUEST)\[',
                    'type': 'input_handling',
                    'severity': 'medium',
                    'description': 'Direct use of user input',
                    'recommendation': 'Sanitize and validate all input'
                },
                {
                    'pattern': r'mysql_query\(',
                    'type': 'sql_injection',
                    'severity': 'high',
                    'description': 'Deprecated MySQL function prone to injection',
                    'recommendation': 'Use PDO with prepared statements'
                },
                {
                    'pattern': r'base64_decode\(',
                    'type': 'obfuscation',
                    'severity': 'medium',
                    'description': 'Base64 decoding often hides malicious code',
                    'recommendation': 'Verify decoded content'
                },
                {
                    'pattern': r'file_get_contents\(["\']http',
                    'type': 'remote_file_inclusion',
                    'severity': 'high',
                    'description': 'Fetching remote files',
                    'recommendation': 'Whitelist allowed URLs'
                }
            ],
            'bash': [
                {
                    'pattern': r'curl.*\|\s*bash',
                    'type': 'remote_code_execution',
                    'severity': 'critical',
                    'description': 'Downloads and executes remote script',
                    'recommendation': 'Never pipe curl to bash'
                },
                {
                    'pattern': r'wget.*\|\s*sh',
                    'type': 'remote_code_execution',
                    'severity': 'critical',
                    'description': 'Downloads and executes remote script',
                    'recommendation': 'Never pipe wget to shell'
                },
                {
                    'pattern': r'nc\s+-[le]',
                    'type': 'backdoor',
                    'severity': 'critical',
                    'description': 'Netcat listener - potential backdoor',
                    'recommendation': 'Remove unauthorized listeners'
                },
                {
                    'pattern': r'/dev/tcp/',
                    'type': 'network_communication',
                    'severity': 'high',
                    'description': 'Direct TCP connection',
                    'recommendation': 'Verify destination'
                },
                {
                    'pattern': r'rm\s+-rf\s+/',
                    'type': 'destructive',
                    'severity': 'critical',
                    'description': 'Recursive deletion from root',
                    'recommendation': 'EXTREMELY DANGEROUS - remove immediately'
                }
            ]
        }
    
    def analyze(self, code: str, language: str = 'python') -> Dict[str, Any]:
        """
        Analyze code for malicious patterns
        Returns: {risk_level, score, threats, ai_analysis}
        """
        threats = []
        
        # Pattern matching
        if self.config['enable_patterns']:
            threats.extend(self._pattern_match(code, language))
        
        # Static analysis for Python
        if self.config['enable_static_analysis'] and language == 'python':
            threats.extend(self._static_analysis_python(code))
        
        # AI analysis
        ai_analysis = ""
        if self.config['enable_ai']:
            ai_analysis = self._ai_analyze(code, language, threats)
        
        # Calculate risk score
        score = self._calculate_risk_score(threats)
        risk_level = self._get_risk_level(score)
        
        return {
            'risk_level': risk_level,
            'score': score,
            'threats': threats,
            'ai_analysis': ai_analysis
        }
    
    def _pattern_match(self, code: str, language: str) -> List[Dict]:
        """Match code against known malicious patterns"""
        threats = []
        patterns = self.patterns.get(language, [])
        
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern_info in patterns:
                if re.search(pattern_info['pattern'], line):
                    threats.append({
                        'type': pattern_info['type'],
                        'severity': pattern_info['severity'],
                        'line': i,
                        'description': pattern_info['description'],
                        'recommendation': pattern_info.get('recommendation', '')
                    })
        
        return threats
    
    def _static_analysis_python(self, code: str) -> List[Dict]:
        """Static analysis for Python using AST"""
        threats = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                # Check for dangerous function calls
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        func_name = node.func.id
                        if func_name in ['eval', 'exec', '__import__']:
                            threats.append({
                                'type': 'dangerous_function',
                                'severity': 'critical',
                                'line': node.lineno,
                                'description': f'Dangerous function {func_name}() detected',
                                'recommendation': 'Remove or replace with safer alternative'
                            })
                
                # Check for suspicious imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in ['subprocess', 'socket', 'ctypes']:
                            threats.append({
                                'type': 'suspicious_import',
                                'severity': 'medium',
                                'line': node.lineno,
                                'description': f'Import of potentially dangerous module: {alias.name}',
                                'recommendation': 'Verify necessity of this import'
                            })
        except SyntaxError:
            pass  # Invalid Python code
        
        return threats
    
    def _ai_analyze(self, code: str, language: str, threats: List[Dict]) -> str:
        """Use Ollama AI to analyze code"""
        try:
            prompt = f"""Analyze this {language} code for malicious or suspicious behavior.
Known threats already detected: {len(threats)}

Code:
```{language}
{code[:2000]}  # Limit to first 2000 chars
```

Provide a brief security assessment (2-3 sentences). Focus on:
1. Overall intent and behavior
2. Any additional concerns not already flagged
3. Confidence level in your assessment"""

            response = requests.post(
                f"{self.config['ollama_url']}/api/generate",
                json={
                    'model': self.config['ai_model'],
                    'prompt': prompt,
                    'stream': False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get('response', '')
        except Exception as e:
            return f"AI analysis unavailable: {str(e)}"
        
        return ""
    
    def _calculate_risk_score(self, threats: List[Dict]) -> int:
        """Calculate risk score 0-100 based on threats"""
        if not threats:
            return 0
        
        severity_weights = {
            'critical': 40,
            'high': 25,
            'medium': 10,
            'low': 5
        }
        
        score = sum(severity_weights.get(t['severity'], 0) for t in threats)
        return min(score, 100)  # Cap at 100
    
    def _get_risk_level(self, score: int) -> str:
        """Convert score to risk level"""
        if score >= 80:
            return 'critical'
        elif score >= 60:
            return 'high'
        elif score >= 30:
            return 'medium'
        else:
            return 'low'
