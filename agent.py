#!/usr/bin/env python3
"""
Malicious Code Detection Agent
Uses AI (CodeLlama via Ollama) + pattern matching to detect malicious code
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import yaml
import os
from detector import MaliciousCodeDetector

app = Flask(__name__)
CORS(app)

# Load config
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize detector
detector = MaliciousCodeDetector(config)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🛡️ Malicious Code Detector</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            color: #764ba2;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        .input-section {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 15px;
            margin-bottom: 20px;
        }
        textarea {
            width: 100%;
            height: 300px;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            resize: vertical;
        }
        select, button {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }
        select {
            background: #f5f5f5;
            border: 2px solid #ddd;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: bold;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .results {
            margin-top: 30px;
            display: none;
        }
        .risk-badge {
            display: inline-block;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: bold;
            margin-bottom: 20px;
            font-size: 1.2em;
        }
        .risk-low { background: #4ade80; color: white; }
        .risk-medium { background: #fbbf24; color: #333; }
        .risk-high { background: #f87171; color: white; }
        .risk-critical { background: #dc2626; color: white; }
        .threat-card {
            background: #f9fafb;
            border-left: 4px solid #dc2626;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
        }
        .threat-type {
            font-weight: bold;
            color: #dc2626;
            text-transform: uppercase;
            font-size: 0.9em;
        }
        .threat-desc {
            margin: 8px 0;
            color: #333;
        }
        .threat-recommendation {
            color: #059669;
            font-style: italic;
        }
        .ai-analysis {
            background: #eff6ff;
            border-left: 4px solid #3b82f6;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #667eea;
            font-size: 1.2em;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Malicious Code Detector</h1>
        <p class="subtitle">AI-powered security analysis for your code</p>
        
        <div class="input-section">
            <textarea id="codeInput" placeholder="Paste your code here for analysis..."></textarea>
            <div>
                <select id="language">
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="php">PHP</option>
                    <option value="bash">Bash</option>
                    <option value="ruby">Ruby</option>
                    <option value="java">Java</option>
                    <option value="c">C</option>
                    <option value="cpp">C++</option>
                </select>
            </div>
        </div>
        
        <button onclick="analyze()" id="analyzeBtn">🔍 Analyze Code</button>
        
        <div id="loading" class="loading" style="display: none;">
            <div class="spinner"></div>
            Analyzing code with AI...
        </div>
        
        <div id="results" class="results"></div>
    </div>

    <script>
        async function analyze() {
            const code = document.getElementById('codeInput').value;
            const language = document.getElementById('language').value;
            const btn = document.getElementById('analyzeBtn');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            
            if (!code.trim()) {
                alert('Please enter some code to analyze');
                return;
            }
            
            btn.disabled = true;
            loading.style.display = 'block';
            results.style.display = 'none';
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ code, language })
                });
                
                const data = await response.json();
                displayResults(data);
            } catch (error) {
                results.innerHTML = `<div class="threat-card"><strong>Error:</strong> ${error.message}</div>`;
                results.style.display = 'block';
            } finally {
                btn.disabled = false;
                loading.style.display = 'none';
            }
        }
        
        function displayResults(data) {
            const results = document.getElementById('results');
            let html = '';
            
            // Risk badge
            const riskClass = `risk-${data.risk_level}`;
            html += `<div class="risk-badge ${riskClass}">
                Risk Level: ${data.risk_level.toUpperCase()} (Score: ${data.score}/100)
            </div>`;
            
            // Threats
            if (data.threats && data.threats.length > 0) {
                html += '<h2>⚠️ Detected Threats</h2>';
                data.threats.forEach(threat => {
                    html += `
                        <div class="threat-card">
                            <div class="threat-type">${threat.type} - ${threat.severity}</div>
                            ${threat.line ? `<div>Line: ${threat.line}</div>` : ''}
                            <div class="threat-desc">${threat.description}</div>
                            ${threat.recommendation ? 
                                `<div class="threat-recommendation">💡 ${threat.recommendation}</div>` : ''}
                        </div>
                    `;
                });
            } else {
                html += '<p style="color: #059669; font-weight: bold;">✅ No threats detected!</p>';
            }
            
            // AI Analysis
            if (data.ai_analysis) {
                html += `
                    <div class="ai-analysis">
                        <h3>🤖 AI Analysis</h3>
                        <p>${data.ai_analysis}</p>
                    </div>
                `;
            }
            
            results.innerHTML = html;
            results.style.display = 'block';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze code for malicious patterns"""
    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'python')
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    result = detector.analyze(code, language)
    return jsonify(result)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ai_enabled': config['enable_ai'],
        'model': config['ai_model']
    })

if __name__ == '__main__':
    print("🛡️  Malicious Code Detector Agent Starting...")
    print(f"🌐 Web Interface: http://localhost:{config['server']['port']}")
    print(f"🤖 AI Model: {config['ai_model']}")
    print(f"📊 Risk Threshold: {config['threshold']}")
    
    app.run(
        host=config['server']['host'],
        port=config['server']['port'],
        debug=config['server']['debug']
    )
