# scanner.py
import os
from dotenv import load_dotenv
from yyds_net_scan import scan_network

load_dotenv()
LAN_SUBNET = os.getenv("LAN_SUBNET", "192.168.1.0/24")

def get_connected_devices(subnet: str = LAN_SUBNET) -> list[dict]:
    """
    Pindai semua perangkat di subnet LAN (default 192.168.1.0/24).
    Return list of dict: IP, MAC, Vendor, Hostname.
    """
    devices = scan_network(subnet)
    out = []
    for d in devices:
        out.append({
            "IP Address": d.ip,
            "MAC Address": d.mac,
            "Vendor": d.vendor,
            "Hostname": d.hostname,
        })
    # urutkan by IP
    try:
        out.sort(key=lambda x: tuple(int(p) for p in x["IP Address"].split(".")))
    except Exception:
        pass
    return out
