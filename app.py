# app.py
import streamlit as st
import pandas as pd
from router import verify_network
from scanner import get_connected_devices, LAN_SUBNET
from speedtest_module import run_speed_test

st.set_page_config(page_title="Network Tools — selese", page_icon="📡", layout="wide")
st.title("📡 Network Tools — Router `selese`")
st.caption(f"Router: 192.168.1.1 · Subnet: {LAN_SUBNET}")

# ---- Cek status jaringan di sidebar ----
with st.sidebar:
    st.header("Status Jaringan")
    if st.button("🔄 Cek Status"):
        st.session_state["net_status"] = verify_network()

    status = st.session_state.get("net_status")
    if status:
        st.write(f"**Hostname:** `{status['hostname']}`")
        st.write(f"**SSID saat ini:** `{status['current_ssid'] or 'tidak terdeteksi'}`")
        if status["ssid_match"] is True:
            st.success(f"✅ Terhubung ke `{status['expected_ssid']}`")
        elif status["ssid_match"] is False:
            st.error(f"⚠️ Terhubung ke `{status['current_ssid']}`, bukan `{status['expected_ssid']}`")
        else:
            st.info("ℹ️ SSID tidak dapat dideteksi di sistem ini")
        st.write(f"**Router 192.168.1.1:** {'🟢 online' if status['router_online'] else '🔴 tidak terjangkau'}")
    else:
        st.info("Klik 'Cek Status' untuk memulai.")

# ---- Tabs ----
tab_scan, tab_speed, tab_about = st.tabs(
    ["🔍 Deteksi Perangkat", "⚡ Tes Kecepatan", "ℹ️ Info & Catatan"]
)

with tab_scan:
    st.header("Perangkat yang Terhubung ke Router `selese`")
    col_a, col_b = st.columns([1, 3])
    with col_a:
        if st.button("▶️ Pindai Sekarang", type="primary"):
            with st.spinner(f"Memindai {LAN_SUBNET} ..."):
                try:
                    devices = get_connected_devices()
                    st.session_state["devices"] = devices
                except Exception as e:
                    st.error(f"Gagal memindai: {e}")

    devices = st.session_state.get("devices")
    if devices is not None:
        if devices:
            df = pd.DataFrame(devices)
            st.success(f"Ditemukan {len(df)} perangkat di {LAN_SUBNET}")
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Unduh CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="perangkat_selese.csv",
                mime="text/csv",
            )
        else:
            st.warning("Tidak ada perangkat terdeteksi. Coba jalankan di komputer yang terhubung ke WiFi `selese`.")

with tab_speed:
    st.header("Tes Kecepatan Internet (via `selese`)")
    if st.button("🚀 Mulai Tes Kecepatan", type="primary"):
        with st.spinner("Mengukur download & upload ... (30–60 detik)"):
            try:
                res = run_speed_test()
                c1, c2, c3 = st.columns(3)
                c1.metric("Download", f"{res['Download (Mbps)']} Mbps")
                c2.metric("Upload", f"{res['Upload (Mbps)']} Mbps")
                c3.metric("Ping", f"{res['Ping (ms)']} ms")
            except Exception as e:
                st.error(f"Tes kecepatan gagal: {e}")

with tab_about:
    st.markdown(f"""
    ### Konfigurasi
    - **Router IP:** `192.168.1.1`
    - **SSID:** `selese`
    - **Subnet scan:** `{LAN_SUBNET}`
    - **Kredensial:** disimpan di `.env` (lokal), **tidak** di-commit ke GitHub

    ### Batasan
    - Fitur deteksi perangkat **hanya berfungsi jika dijalankan di komputer yang terhubung ke WiFi `selese`**.
    - Di GitHub Codespaces (cloud) atau Streamlit Cloud, hasil scan akan menampilkan perangkat di **subnet cloud**, bukan rumah Anda.
    - Login ke panel admin router (192.168.1.1) **tidak** dilakukan karena berbeda-beda per vendor. Jika perlu, tambahkan modul `requests` khusus sesuai merek router (TP-Link, MikroTik, ZTE, dsb).
    """)
