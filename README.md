# 📡 Network Tools — Router `selese`

Aplikasi dashboard berbasis **Python + Streamlit** untuk:

1. 🔍 **Mendeteksi perangkat** yang terhubung ke jaringan lokal router `selese` (`192.168.1.0/24`)
2. ⚡ **Mengukur kecepatan internet** (download, upload, ping) melalui koneksi router tersebut
3. 🩺 **Memeriksa status router** (`192.168.1.1`) — online/offline & kecocokan SSID

Dikembangkan menggunakan **GitHub Codespaces** sebagai editor, tetapi **dijalankan secara lokal** agar dapat memindai jaringan rumah.

---

## 📋 Daftar Isi

- [Fitur](#-fitur)
- [Arsitektur](#-arsitektur)
- [Prasyarat](#-prasyarat)
- [Instalasi](#-instalasi)
- [Konfigurasi](#-konfigurasi)
- [Menjalankan Aplikasi](#-menjalankan-aplikasi)
- [Struktur Proyek](#-struktur-proyek)
- [Batasan Penting](#-batasan-penting)
- [Keamanan](#-keamanan)
- [Troubleshooting](#-troubleshooting)
- [Lisensi](#-lisensi)

---

## ✨ Fitur

| Fitur | Deskripsi |
|---|---|
| **Deteksi Perangkat** | Memindai subnet `192.168.1.0/24` dan menampilkan IP, MAC address, vendor, serta hostname setiap perangkat yang aktif |
| **Tes Kecepatan** | Mengukur download (Mbps), upload (Mbps), dan ping (ms) menggunakan server Speedtest.net terdekat |
| **Cek Status Router** | Ping router `192.168.1.1` dan verifikasi apakah perangkat sedang terhubung ke SSID `selese` |
| **Ekspor CSV** | Hasil pemindaian perangkat dapat diunduh sebagai file CSV |
| **Dashboard Multi-Tab** | Antarmuka Streamlit dengan tab terpisah untuk setiap fitur |

---

## 🏗 Arsitektur
