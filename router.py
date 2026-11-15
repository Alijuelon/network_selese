# router.py
import os
import subprocess
import platform
import socket
from dotenv import load_dotenv

load_dotenv()

ROUTER_IP = os.getenv("ROUTER_IP", "192.168.1.1")
EXPECTED_SSID = os.getenv("ROUTER_SSID", "selese")

def ping_router(ip: str = ROUTER_IP, count: int = 3) -> dict:
    """Ping router untuk cek apakah online & ukur latency."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", param, str(count), ip],
            capture_output=True, text=True, timeout=10
        )
        alive = result.returncode == 0
        # ambil latency rata-rata (parsing sederhana)
        latency = None
        for line in result.stdout.splitlines():
            if "avg" in line.lower() or "average" in line.lower():
                latency = line.strip()
                break
        return {"router_ip": ip, "online": alive, "raw": latency or result.stdout[-200:]}
    except Exception as e:
        return {"router_ip": ip, "online": False, "raw": str(e)}

def get_current_ssid() -> str | None:
    """
    Ambil nama WiFi yang sedang terhubung.
    - Windows: netsh wlan show interfaces
    - Linux:   nmcli -t -f active,ssid dev wifi
    - macOS:   /System/Library/PrivateFrameworks/Apple80211.framework/.../airport -I
    """
    system = platform.system().lower()
    try:
        if system == "windows":
            out = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"],
                text=True, encoding="utf-8", errors="ignore"
            )
            for line in out.splitlines():
                if "SSID" in line and "BSSID" not in line:
                    return line.split(":", 1)[1].strip()
        elif system == "linux":
            out = subprocess.check_output(
                ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"],
                text=True
            )
            for line in out.splitlines():
                if line.startswith("yes:"):
                    return line.split(":", 1)[1]
        elif system == "darwin":
            out = subprocess.check_output(
                ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
                text=True
            )
            for line in out.splitlines():
                if " SSID:" in line:
                    return line.split(":", 1)[1].strip()
    except Exception:
        return None
    return None

def verify_network() -> dict:
    """Ringkasan: apakah terhubung ke SSID yang diharapkan + status router."""
    ssid = get_current_ssid()
    router = ping_router()
    return {
        "expected_ssid": EXPECTED_SSID,
        "current_ssid": ssid,
        "ssid_match": (ssid == EXPECTED_SSID) if ssid else None,
        "router_online": router["online"],
        "router_ip": router["router_ip"],
        "hostname": socket.gethostname(),
    }
