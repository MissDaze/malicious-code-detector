#!/usr/bin/env python3
"""
CLI interface for malicious code detection
"""

import click
import yaml
import os
import sys
from pathlib import Path
from colorama import init, Fore, Style
from detector import MaliciousCodeDetector
import time

init(autoreset=True)

# Load config
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

detector = MaliciousCodeDetector(config)

def print_banner():
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════╗
║   🛡️  Malicious Code Detector CLI   ║
╚══════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

def print_result(result):
    """Pretty print analysis result"""
    risk_colors = {
        'low': Fore.GREEN,
        'medium': Fore.YELLOW,
        'high': Fore.RED,
        'critical': Fore.RED + Style.BRIGHT
    }
    
    color = risk_colors.get(result['risk_level'], Fore.WHITE)
    
    print(f"\n{color}{'='*60}")
    print(f"Risk Level: {result['risk_level'].upper()} (Score: {result['score']}/100)")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    if result['threats']:
        print(f"{Fore.YELLOW}⚠️  Detected Threats:{Style.RESET_ALL}\n")
        for threat in result['threats']:
            severity_color = {
                'critical': Fore.RED + Style.BRIGHT,
                'high': Fore.RED,
                'medium': Fore.YELLOW,
                'low': Fore.CYAN
            }.get(threat['severity'], Fore.WHITE)
            
            print(f"{severity_color}[{threat['severity'].upper()}] {threat['type']}{Style.RESET_ALL}")
            print(f"  Line: {threat.get('line', 'N/A')}")
            print(f"  {threat['description']}")
            if threat.get('recommendation'):
                print(f"  {Fore.GREEN}💡 {threat['recommendation']}{Style.RESET_ALL}")
            print()
    else:
        print(f"{Fore.GREEN}✅ No threats detected!{Style.RESET_ALL}\n")
    
    if result['ai_analysis']:
        print(f"{Fore.CYAN}🤖 AI Analysis:{Style.RESET_ALL}")
        print(f"{result['ai_analysis']}\n")

@click.group()
def cli():
    """Malicious Code Detection CLI"""
    print_banner()

@cli.command()
@click.option('--file', '-f', required=True, help='File to analyze')
@click.option('--language', '-l', help='Programming language (auto-detect if not provided)')
def analyze(file, language):
    """Analyze a single file for malicious code"""
    if not os.path.exists(file):
        print(f"{Fore.RED}Error: File '{file}' not found{Style.RESET_ALL}")
        sys.exit(1)
    
    # Auto-detect language from extension
    if not language:
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.php': 'php',
            '.sh': 'bash',
            '.rb': 'ruby',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'cpp',
            '.cc': 'cpp'
        }
        ext = Path(file).suffix
        language = ext_map.get(ext, 'python')
    
    print(f"{Fore.CYAN}📄 Analyzing: {file}")
    print(f"🔤 Language: {language}{Style.RESET_ALL}\n")
    
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        code = f.read()
    
    print(f"{Fore.YELLOW}⏳ Running analysis...{Style.RESET_ALL}")
    result = detector.analyze(code, language)
    print_result(result)

@cli.command()
@click.option('--dir', '-d', required=True, help='Directory to scan')
@click.option('--recursive/--no-recursive', default=True, help='Scan subdirectories')
@click.option('--extensions', '-e', multiple=True, help='File extensions to scan (e.g., .py .js)')
def scan(dir, recursive, extensions):
    """Scan a directory for malicious code"""
    if not os.path.isdir(dir):
        print(f"{Fore.RED}Error: Directory '{dir}' not found{Style.RESET_ALL}")
        sys.exit(1)
    
    # Default extensions
    if not extensions:
        extensions = ['.py', '.js', '.php', '.sh', '.rb', '.java', '.c', '.cpp']
    
    print(f"{Fore.CYAN}📁 Scanning directory: {dir}")
    print(f"🔍 Recursive: {recursive}")
    print(f"📝 Extensions: {', '.join(extensions)}{Style.RESET_ALL}\n")
    
    # Find files
    files = []
    path = Path(dir)
    
    if recursive:
        for ext in extensions:
            files.extend(path.rglob(f'*{ext}'))
    else:
        for ext in extensions:
            files.extend(path.glob(f'*{ext}'))
    
    if not files:
        print(f"{Fore.YELLOW}No files found with specified extensions{Style.RESET_ALL}")
        return
    
    print(f"Found {len(files)} file(s) to analyze\n")
    
    high_risk_files = []
    total_threats = 0
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            # Detect language
            ext = file_path.suffix
            lang_map = {
                '.py': 'python', '.js': 'javascript', '.php': 'php',
                '.sh': 'bash', '.rb': 'ruby', '.java': 'java',
                '.c': 'c', '.cpp': 'cpp', '.cc': 'cpp'
            }
            language = lang_map.get(ext, 'python')
            
            result = detector.analyze(code, language)
            
            if result['score'] > 0:
                rel_path = file_path.relative_to(path)
                risk_color = {
                    'low': Fore.GREEN,
                    'medium': Fore.YELLOW,
                    'high': Fore.RED,
                    'critical': Fore.RED + Style.BRIGHT
                }.get(result['risk_level'], Fore.WHITE)
                
                print(f"{risk_color}{'⚠️ ' if result['risk_level'] in ['high', 'critical'] else '📝 '}"
                      f"{rel_path} - {result['risk_level'].upper()} ({result['score']}/100){Style.RESET_ALL}")
                
                if result['risk_level'] in ['high', 'critical']:
                    high_risk_files.append((str(rel_path), result))
                
                total_threats += len(result['threats'])
        
        except Exception as e:
            print(f"{Fore.RED}Error analyzing {file_path}: {e}{Style.RESET_ALL}")
    
    # Summary
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"Scan Complete")
    print(f"{'='*60}{Style.RESET_ALL}")
    print(f"Files scanned: {len(files)}")
    print(f"Total threats: {total_threats}")
    print(f"High-risk files: {len(high_risk_files)}\n")
    
    if high_risk_files:
        print(f"{Fore.RED}⚠️  HIGH RISK FILES:{Style.RESET_ALL}\n")
        for file, result in high_risk_files:
            print(f"{Fore.RED}📄 {file}{Style.RESET_ALL}")
            for threat in result['threats'][:3]:  # Show first 3 threats
                print(f"   • {threat['type']}: {threat['description']}")
            print()

@cli.command()
@click.option('--dir', '-d', required=True, help='Directory to watch')
@click.option('--interval', '-i', default=5, help='Check interval in seconds')
def watch(dir, interval):
    """Watch a directory for changes and analyze new/modified files"""
    if not os.path.isdir(dir):
        print(f"{Fore.RED}Error: Directory '{dir}' not found{Style.RESET_ALL}")
        sys.exit(1)
    
    print(f"{Fore.CYAN}👁️  Watching: {dir}")
    print(f"⏱️  Interval: {interval}s")
    print(f"Press Ctrl+C to stop{Style.RESET_ALL}\n")
    
    watched_files = {}
    
    try:
        while True:
            path = Path(dir)
            for file_path in path.rglob('*'):
                if file_path.is_file() and file_path.suffix in ['.py', '.js', '.php', '.sh']:
                    mtime = file_path.stat().st_mtime
                    
                    if file_path not in watched_files or watched_files[file_path] != mtime:
                        watched_files[file_path] = mtime
                        
                        # Analyze file
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                code = f.read()
                            
                            ext = file_path.suffix
                            lang_map = {'.py': 'python', '.js': 'javascript', '.php': 'php', '.sh': 'bash'}
                            language = lang_map.get(ext, 'python')
                            
                            result = detector.analyze(code, language)
                            
                            if result['score'] >= config['threshold']:
                                print(f"\n{Fore.YELLOW}⚠️  New threat detected: {file_path.name}{Style.RESET_ALL}")
                                print_result(result)
                        
                        except Exception as e:
                            pass
            
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}👋 Stopped watching{Style.RESET_ALL}")

if __name__ == '__main__':
    cli()
