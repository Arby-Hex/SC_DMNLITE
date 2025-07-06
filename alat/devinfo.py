import os
import platform
import socket
import getpass
import subprocess
import time

# Auto Install
def auto_install():
    try:
        import requests, netifaces, psutil
    except ImportError:
        os.system("pip install requests netifaces psutil")

auto_install()
import requests
import netifaces
import psutil

# Warna
GREEN = "\033[92m"
RESET = "\033[0m"

# Banner ASCII Manual
def banner():
    os.system("clear")
    print(GREEN + r"""
╔═╗╔═╗╔═╗╦═╗╔═╗╔╦╗  ╔╦╗╔═╗╔═╗╔╦╗╔═╗╔╗╔╦╦ ╦╔╦╗
╚═╗║╣ ║  ╠╦╝║╣  ║    ║║╠═╣║╣ ║║║║ ║║║║║║ ║║║║
╚═╝╚═╝╚═╝╩╚═╚═╝ ╩   ═╩╝╩ ╩╚═╝╩ ╩╚═╝╝╚╝╩╚═╝╩ ╩

::=========[ ☠ DEVICE INFO ☠ ]=========::
""" + RESET)

# IP Publik
def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Tidak dapat terhubung"

# IP Lokal
def get_local_ip():
    try:
        gws = netifaces.gateways()
        default_interface = gws['default'][netifaces.AF_INET][1]
        return netifaces.ifaddresses(default_interface)[netifaces.AF_INET][0]['addr']
    except:
        return "Tidak ditemukan"

# Lokasi dari IP
def get_geo_location(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}").json()
        return f"{r['country']}, {r['regionName']}, {r['city']}"
    except:
        return "Tidak tersedia"

def get_storage():
    try:
        path = os.path.expanduser("~")  # Direktori home Termux
        usage = psutil.disk_usage(path)
        total = usage.total // (2**30)
        free = usage.free // (2**30)
        return f"Total: {total} GB | Bebas: {free} GB"
    except Exception as e:
        return f"Gagal deteksi: {e}"

# RAM
def get_ram():
    ram = psutil.virtual_memory()
    return f"Total: {ram.total // (2**20)} MB | Tersedia: {ram.available // (2**20)} MB"

def get_cpu_info():
    try:
        with open("/proc/cpuinfo", "r") as f:
            info = f.read()
            for line in info.split("\n"):
                if "Hardware" in line or "Processor" in line or "model name" in line:
                    return line.split(":")[1].strip()
        return "Tidak terdeteksi"
    except:
        return "Tidak tersedia"

# MAC Address
def get_mac():
    try:
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_LINK in addrs:
                mac = addrs[netifaces.AF_LINK][0]['addr']
                if mac != '00:00:00:00:00:00':
                    return mac
    except:
        return "Tidak ditemukan"
    return "Tidak ditemukan"

# Model Device Android
def get_device_model():
    try:
        return subprocess.check_output("getprop ro.product.model", shell=True).decode().strip()
    except:
        return "Tidak diketahui"

# Waktu & Zona
def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime())

# Fungsi Utama
def run():
    banner()
    public_ip = get_public_ip()
    print(f"{GREEN}📱 Model Perangkat  :{RESET} {get_device_model()}")
    print(f"{GREEN}👤 Username         :{RESET} {getpass.getuser()}")
    print(f"{GREEN}🧠 Hostname         :{RESET} {socket.gethostname()}")
    print(f"{GREEN}💻 Sistem Operasi   :{RESET} {platform.system()} {platform.release()}")
    print(f"{GREEN}🖥️ Arsitektur CPU    :{RESET} {get_cpu_info()}")
    print(f"{GREEN}💾 RAM              :{RESET} {get_ram()}")
    print(f"{GREEN}📂 Penyimpanan      :{RESET} {get_storage()}")
    print(f"{GREEN}🌐 IP Publik        :{RESET} {public_ip}")
    print(f"{GREEN}🏠 IP Lokal         :{RESET} {get_local_ip()}")
    print(f"{GREEN}🌍 Lokasi (IP)      :{RESET} {get_geo_location(public_ip)}")
    print(f"{GREEN}🔒 MAC Address      :{RESET} {get_mac()}")
    print(f"{GREEN}🕐 Waktu Sekarang   :{RESET} {get_time()}")
    print("-" * 50)
    input(f"{GREEN}Tekan Enter Untuk Kembali...{RESET}")

# Jika dijalankan langsung
if __name__ == "__main__":
    run()
