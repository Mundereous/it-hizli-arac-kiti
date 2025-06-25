import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import os
import json
from datetime import datetime

USE_DARK_THEME = True

THEME = {
    "bg": "#1e1e1e" if USE_DARK_THEME else "#f0f0f0",
    "fg": "#ffffff" if USE_DARK_THEME else "#000000",
    "button_bg": "#2d2d30" if USE_DARK_THEME else "#ffffff",
    "button_fg": "#ffffff" if USE_DARK_THEME else "#333333",
    "hover": "#3e3e42" if USE_DARK_THEME else "#d0eaff"
}

ICONS = {
    "system": "🖥", "network": "🌐", "disk": "🗝", "user": "👤", "info": "ℹ️",
    "wifi": "📶", "ram": "🧠", "cpu": "⚙️", "firewall": "🛡", "update": "🔄",
    "tools": "🛠", "exit": "❌"
}

LOG_FILE = "linux_toolkit_log.json"

def log_result(action_name, output, success=True):
    entry = {
        "timestamp": datetime.now().isoformat(timespec='seconds'),
        "action": action_name,
        "success": success,
        "output": output
    }
    data = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            pass
    data.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def run_cmd(title, cmd):
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        messagebox.showinfo(title, result)
        log_result(title, result, True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror(title, e.output)
        log_result(title, e.output, False)

# Ana fonksiyonlar

def chkrootkit(): run_cmd("Chkrootkit Taraması", "sudo chkrootkit")
def top_processes(): run_cmd("TOP Süreçleri", "top -n 1 -b | head -20")
def flatpak_cleanup(): run_cmd("Flatpak Temizle", "flatpak uninstall --unused -y")
def snap_cleanup(): run_cmd("Snap Temizle", "sudo snap set system refresh.retain=2 && sudo snap remove --purge $(snap list --all | awk '/disabled/{print $1, $3}')")
def change_password(): 
    user = simpledialog.askstring("Şifre Değiştir", "Hangi kullanıcı?")
    if user:
        run_cmd("Şifre Değiştir", f"sudo passwd {user}")
def search_package():
    package = simpledialog.askstring("Paket Ara", "Paket ismi:")
    if package:
        run_cmd("Paket Arama", f"apt search {package}")

def gui_main():
    root = tk.Tk()
    root.title("🛠 Linux Araç Kiti")
    root.configure(bg=THEME['bg'])
    root.geometry("1280x800")

    title_label = tk.Label(root, text="🛠 Linux Hızlı Araç Kiti", font=("Segoe UI", 26, "bold"), bg=THEME['bg'], fg=THEME['fg'], pady=20)
    title_label.pack()

    frame = tk.Frame(root, bg=THEME['bg'])
    frame.pack(padx=20, pady=10, fill="both", expand=True)

    features = [
        ("IP Bilgisi", lambda: run_cmd("IP Bilgisi", "ip a"), ICONS["network"]),
        ("Route Tablosu", lambda: run_cmd("Route", "ip route"), ICONS["network"]),
        ("Kullanıcıları Listele", lambda: run_cmd("Kullanıcılar", "cut -d: -f1 /etc/passwd"), ICONS["user"]),
        ("Disk Kullanımı", lambda: run_cmd("Disk Kullanımı", "df -h"), ICONS["disk"]),
        ("CPU Bilgisi", lambda: run_cmd("CPU Bilgisi", "lscpu"), ICONS["cpu"]),
        ("RAM Bilgisi", lambda: run_cmd("RAM", "free -h"), ICONS["ram"]),
        ("Ping", lambda: run_cmd("Ping", f"ping -c 4 {simpledialog.askstring('Ping', 'Hedef adres:')}"), ICONS["network"]),
        ("Traceroute", lambda: run_cmd("Traceroute", f"traceroute {simpledialog.askstring('Traceroute', 'Hedef adres:')}"), ICONS["network"]),
        ("Açık Portlar", lambda: run_cmd("Portlar", "ss -tulnp"), ICONS["network"]),
        ("Sistem Bilgisi", lambda: run_cmd("Sistem", "uname -a"), ICONS["system"]),
        ("Paketleri Güncelle", lambda: run_cmd("Update", "sudo apt update && sudo apt upgrade -y"), ICONS["update"]),
        ("DNS Temizle", lambda: run_cmd("DNS", "sudo systemd-resolve --flush-caches"), ICONS["network"]),
        ("Logları Temizle", lambda: run_cmd("Log Temizle", "sudo journalctl --rotate && sudo journalctl --vacuum-time=2d"), ICONS["tools"]),
        ("/tmp Temizle", lambda: run_cmd("/tmp Temizle", "sudo rm -rf /tmp/*"), ICONS["tools"]),
        ("Aktif Kullanıcı", lambda: run_cmd("Kullanıcı", "whoami"), ICONS["user"]),
        ("Uptime", lambda: run_cmd("Uptime", "uptime"), ICONS["info"]),
        ("Chkrootkit", chkrootkit, ICONS["firewall"]),
        ("TOP Süreçleri", top_processes, ICONS["cpu"]),
        ("Flatpak Temizle", flatpak_cleanup, ICONS["disk"]),
        ("Snap Temizle", snap_cleanup, ICONS["disk"]),
        ("Şifre Değiştir", change_password, ICONS["user"]),
        ("Paket Ara", search_package, ICONS["tools"]),
        ("Çık", root.quit, ICONS["exit"])
    ]

    def on_enter(e): e.widget['background'] = THEME['hover']
    def on_leave(e): e.widget['background'] = THEME['button_bg']

    for idx, (text, func, icon) in enumerate(features):
        row, col = divmod(idx, 3)
        btn = tk.Button(
            frame,
            text=f"{icon}  {text}",
            width=40,
            height=2,
            command=func,
            font=("Segoe UI", 11, "bold"),
            bg=THEME['button_bg'],
            fg=THEME['button_fg'],
            relief="flat",
            bd=0,
            activebackground=THEME['hover'],
            activeforeground=THEME['button_fg'],
            anchor="w",
            padx=15
        )
        btn.grid(row=row, column=col, padx=10, pady=8, sticky="ew")
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    for i in range(3):
        frame.grid_columnconfigure(i, weight=1)

    root.mainloop()

if __name__ == "__main__":
    gui_main()
