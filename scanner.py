# scanner.py
from yyds_net_scan import scan_network

# ====== KONFIGURASI LANGSUNG ======
LAN_SUBNET = "192.168.1.0/24"
SCAN_PORTS = "top20"      # "top20", "top100", atau "80,443,8080"
SCAN_TIMEOUT = 0.8        # detik
# ==================================

def get_connected_devices(subnet: str = LAN_SUBNET) -> list[dict]:
    """
    Pindai subnet LAN dan kembalikan list of dict.
    CATATAN: scan_network() mengembalikan ScanReport, bukan list.
    Perangkat ada di report.hosts.
    """
    report = scan_network(subnet, ports=SCAN_PORTS, timeout=SCAN_TIMEOUT)

    out = []
    for host in report.hosts:          # <-- INI KUNCI PERBAIKANNYA
        out.append({
            "IP Address": host.ip,
            "MAC Address": host.mac,
            "Vendor": host.vendor,
            "Hostname": host.hostname,
            "Open Ports": host.ports_display(),
        })

    # urutkan berdasarkan IP
    try:
        out.sort(key=lambda x: tuple(int(p) for p in x["IP Address"].split(".")))
    except Exception:
        pass

    return out
