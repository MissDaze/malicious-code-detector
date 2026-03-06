# Installation Guide

## Quick Start (5 minutes)

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Ollama (for AI analysis)

**Linux/macOS:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from https://ollama.ai/download

### 3. Download AI Model

```bash
ollama pull codellama:7b
```

This downloads a 4GB model. Wait for it to complete.

### 4. Start the Agent

```bash
python agent.py
```

Open http://localhost:5000 in your browser!

## Alternative Models

If CodeLlama is too large, use smaller models:

```bash
# Smaller, faster (2GB)
ollama pull codellama:7b-code

# Tiny model for testing (1GB)
ollama pull tinyllama
```

Edit `config.yaml` to change the model:
```yaml
ai_model: tinyllama
```

## Docker Setup (Optional)

```bash
docker build -t malicious-code-detector .
docker run -p 5000:5000 malicious-code-detector
```

## Troubleshooting

**Ollama not found:**
- Ensure Ollama is installed and running: `ollama list`
- Start Ollama service: `ollama serve`

**Port 5000 already in use:**
Edit `config.yaml` and change the port:
```yaml
server:
  port: 8080
```

**Python dependencies fail:**
Try using a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Without AI (Pattern Matching Only)

Don't want to install Ollama? Disable AI in `config.yaml`:

```yaml
enable_ai: false
```

The detector will still work using pattern matching and static analysis!
