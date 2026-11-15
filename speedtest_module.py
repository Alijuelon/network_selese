# speedtest_module.py
import speedtest

def run_speed_test():
    st = speedtest.Speedtest()
    st.get_best_server()
    down = st.download() / 1_000_000
    up = st.upload() / 1_000_000
    ping = st.results.ping
    return {
        "Download (Mbps)": round(down, 2),
        "Upload (Mbps)": round(up, 2),
        "Ping (ms)": round(ping, 2),
    }
