import tkinter as tk
from tkinter import messagebox, simpledialog
import ctypes
import os
import json
from datetime import datetime
from modules.common import run_cmd, run_powershell

# Tema kontrolü
USE_DARK_THEME = True

# Tema renkleri
THEME = {
    "bg": "#1e1e1e" if USE_DARK_THEME else "#f0f0f0",
    "fg": "#ffffff" if USE_DARK_THEME else "#000000",
    "button_bg": "#2d2d30" if USE_DARK_THEME else "#ffffff",
    "button_fg": "#ffffff" if USE_DARK_THEME else "#333333",
    "hover": "#3e3e42" if USE_DARK_THEME else "#d0eaff"
}

ICONS = {
    "system": "🖥", "network": "🌐", "disk": "💽", "user": "👤", "info": "ℹ️",
    "wifi": "📶", "ram": "🧠", "cpu": "⚙️", "firewall": "🛡", "update": "🔄",
    "tools": "🛠", "exit": "❌"
}

LOG_FILE = "it_arac_kit_log.json"

def log_result(action_name, output, success=True):
    """İşlem sonucunu JSON dosyasına kaydeder."""
    entry = {
        "timestamp": datetime.now().isoformat(timespec='seconds'),
        "action": action_name,
        "success": success,
        "output": output
    }
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def simple_run(title, cmd, use_powershell=False):
    code, out, err = run_cmd(cmd, use_powershell=use_powershell)
    success = (code == 0)
    message = out if success else err
    messagebox.showinfo(title, message)
    log_result(title, message, success)

def powershell_run(title, ps_cmd):
    code, out, err = run_powershell(ps_cmd)
    success = (code == 0)
    message = out if success else err
    messagebox.showinfo(title, message)
    log_result(title, message, success)

def gpupdate():
    simple_run("Grup Politikası", ["gpupdate", "/force"])

def show_ip():
    simple_run("IP Bilgisi", ["ipconfig", "/all"])

def show_product_key():
    ps_script = """
    function Get-WindowsKey {
        $key = "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion"
        $digitalProductId = (Get-ItemProperty -Path $key).DigitalProductId
        function ConvertTo-Key($digitalProductId) {
            $key = ""
            $chars = "BCDFGHJKMPQRTVWXY2346789"
            $isWin8 = ($digitalProductId[66] -band 0x80) -ne 0
            if ($isWin8) {
                $digitalProductId[66] = ($digitalProductId[66] -band 0x7F)
                $keyChars = 29
                $keyOffset = 52
            } else {
                $keyChars = 25
                $keyOffset = 52
            }
            for ($i = $keyChars - 1; $i -ge 0; $i--) {
                $current = 0
                for ($j = 14; $j -ge 0; $j--) {
                    $current = $current * 256 -bxor $digitalProductId[$j + $keyOffset]
                    $digitalProductId[$j + $keyOffset] = [math]::Floor($current / 24)
                    $current = $current % 24
                }
                $key = $chars[$current] + $key
                if (($i % 5) -eq 0 -and $i -ne 0) {
                    $key = "-" + $key
                }
            }
            return $key
        }
        ConvertTo-Key $digitalProductId
    }
    Get-WindowsKey
    """
    powershell_run("Windows Ürün Anahtarı", ps_script)

def show_nbtstat():
    simple_run("NBTSTAT", ["nbtstat", "-n"])

def show_wifi():
    result = ""
    code, out, err = run_cmd("netsh wlan show profiles", use_powershell=True)
    if code != 0:
        messagebox.showerror("Hata", err)
        log_result("Wi-Fi Şifreleri", err, False)
        return
    profiles = []
    for line in out.splitlines():
        if "All User Profile" in line:
            parts = line.split(":")
            if len(parts) == 2:
                profiles.append(parts[1].strip())
    for profile in profiles:
        cmd = f'netsh wlan show profile name="{profile}" key=clear'
        code2, out2, err2 = run_cmd(cmd, use_powershell=True)
        if code2 != 0:
            result += f"{profile}: HATA\n"
            continue
        for line2 in out2.splitlines():
            if "Key Content" in line2:
                pwd = line2.split(":")[1].strip()
                result += f"{profile}: {pwd}\n"
                break
    messagebox.showinfo("Wi-Fi Şifreleri", result or "Şifre bulunamadı.")
    log_result("Wi-Fi Şifreleri", result or "Şifre bulunamadı.", True)

def show_format_date():
    try:
        ts = os.stat(r"C:\\Windows").st_ctime
        dt = datetime.fromtimestamp(ts)
        messagebox.showinfo("Son Format Tarihi", str(dt))
        log_result("Son Format Tarihi", str(dt), True)
    except Exception as e:
        messagebox.showerror("Hata", str(e))
        log_result("Son Format Tarihi", str(e), False)

def disk_status():
    simple_run("Disk Durumu", "chkdsk C: /scan", use_powershell=True)

def update_status():
    messagebox.showinfo("Bilgi", "PSWindowsUpdate modülü gerekebilir.")

def cpu_info():
    powershell_run("CPU Bilgisi", "Get-CimInstance Win32_Processor | Select Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed")

def ram_usage():
    powershell_run("RAM Bilgisi", "Get-CimInstance Win32_OperatingSystem | Select TotalVisibleMemorySize,FreePhysicalMemory")

def serial_model():
    powershell_run("Seri No", "Get-CimInstance Win32_BIOS | Select SerialNumber")
    powershell_run("Model", "Get-CimInstance Win32_ComputerSystem | Select Manufacturer,Model,Name")

def list_users():
    powershell_run("Kullanıcılar", "Get-CimInstance Win32_UserAccount | Where-Object {$_.LocalAccount -eq $true} | Select Name,FullName,Disabled")

def storage_status():
    ps_cmd = """
    Get-CimInstance Win32_LogicalDisk | 
    Select-Object DeviceID,
                  @{Name='Size(GB)';Expression={[math]::Round($_.Size/1GB,2)}},
                  @{Name='FreeSpace(GB)';Expression={[math]::Round($_.FreeSpace/1GB,2)}}
    """
    powershell_run("Diskler (GB)", ps_cmd)

def scan_disk():
    drive = simpledialog.askstring("Sürücü", "Hangi sürücü taransın? (örn. C)")
    if drive:
        simple_run("Disk Tarama", f"chkdsk {drive}: /scan", use_powershell=True)

def update_store():
    powershell_run("Store Güncelle", "Get-AppxPackage -AllUsers | Foreach { Add-AppxPackage -DisableDevelopmentMode -Register \"$($_.InstallLocation)\\AppXManifest.xml\" }")

def flush_dns():
    simple_run("DNS Temizle", ["ipconfig", "/flushdns"])

def repair_sfc():
    simple_run("SFC", ["sfc", "/scannow"])

def disk_cleanup():
    os.system("cleanmgr")

def update_all():
    simple_run("Tüm Güncellemeler", ["winget", "upgrade", "--all", "--silent"])

def firewall_off():
    powershell_run("Güvenlik Duvarı Kapat", "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False")

def firewall_on():
    powershell_run("Güvenlik Duvarını Aç", "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True")

def clean_temp():
    temp = os.environ.get("TEMP")
    if not temp:
        messagebox.showerror("Hata", "TEMP klasörü bulunamadı.")
        log_result("Gereksiz Dosyaları Temizle", "TEMP klasörü bulunamadı.", False)
        return
    import time, shutil
    now = time.time()
    cutoff = now - 7 * 86400
    deleted = 0
    for root, dirs, files in os.walk(temp):
        for name in files:
            fp = os.path.join(root, name)
            try:
                if os.path.getmtime(fp) < cutoff:
                    os.remove(fp)
                    deleted += 1
            except:
                pass
        for name in dirs:
            dp = os.path.join(root, name)
            try:
                if os.path.getmtime(dp) < cutoff:
                    shutil.rmtree(dp, ignore_errors=True)
                    deleted += 1
            except:
                pass
    messagebox.showinfo("Gereksiz Dosyalar", f"Silinen öğe sayısı: {deleted}")
    log_result("Gereksiz Dosyaları Temizle", f"Silinen öğe sayısı: {deleted}", True)

def optimize_ram():
    messagebox.showinfo("RAM Optimizasyonu", "Windows RAM yönetimini kendi yapar.")

def ping_test():
    host = simpledialog.askstring("Ping", "Adres girin (örn. 8.8.8.8):")
    if host:
        simple_run("Ping", ["ping", "-n", "4", host])

def tracert_test():
    host = simpledialog.askstring("Tracert", "Adres girin:")
    if host:
        simple_run("Tracert", ["tracert", host])

def nslookup_test():
    host = simpledialog.askstring("Nslookup", "Adres girin:")
    if host:
        simple_run("Nslookup", ["nslookup", host])

def netstat():
    simple_run("Netstat", ["netstat", "-ano"])

def arp():
    simple_run("ARP", ["arp", "-a"])

def route():
    simple_run("Route", ["route", "print"])

def sys_info():
    powershell_run("Sistem Bilgisi", "Get-ComputerInfo | Select CsName,OsName,OsVersion,OsArchitecture,OsBuildNumber")

def ip_config():
    simple_run("IP Config", ["ipconfig", "/all"])

def release_ip():
    simple_run("IP Serbest", ["ipconfig", "/release"])

def renew_ip():
    simple_run("IP Yenile", ["ipconfig", "/renew"])

def win_version():
    powershell_run("Windows Sürümü", "Get-ComputerInfo | Select WindowsVersion,WindowsBuildLabEx")

def on_enter(e):
    e.widget['background'] = THEME['hover']

def on_leave(e):
    e.widget['background'] = THEME['button_bg']

def gui_main():
    if not is_admin():
        messagebox.showwarning("Yönetici Uyarısı", "Lütfen uygulamayı yönetici olarak çalıştırın.")

    root = tk.Tk()
    root.title("🛠 IT Hızlı Araç Kiti - Windows")
    root.geometry("1280x920")
    root.configure(bg=THEME['bg'])
    root.resizable(True, True)

    title_label = tk.Label(
        root,
        text="🛠 IT Hızlı Araç Kiti - Windows",
        font=("Segoe UI Semibold", 26, "bold"),
        bg=THEME['bg'],
        fg=THEME['fg'],
        pady=20
    )
    title_label.pack()

    frame = tk.Frame(root, bg=THEME['bg'])
    frame.pack(padx=20, pady=10, fill="both", expand=True)

    features = [
        ("1. Grup Politikası Güncelle", gpupdate, ICONS["update"]),
        ("2. IP Göster", show_ip, ICONS["network"]),
        ("3. Windows Lisans Anahtarı Göster", show_product_key, ICONS["info"]),
        ("4. Nbtstat Göster", show_nbtstat, ICONS["network"]),
        ("5. Wi-Fi Şifrelerini Göster", show_wifi, ICONS["wifi"]),
        ("6. Son Format Tarihini Göster", show_format_date, ICONS["disk"]),
        ("7. Disk Durumunu Kontrol Et", disk_status, ICONS["disk"]),
        ("8. Windows Güncelleme Durumu", update_status, ICONS["update"]),
        ("9. CPU Bilgilerini Göster", cpu_info, ICONS["cpu"]),
        ("10. RAM Kullanımını Göster", ram_usage, ICONS["ram"]),
        ("11. Seri No, Marka, Model", serial_model, ICONS["system"]),
        ("12. Kullanıcı Hesaplarını Listele", list_users, ICONS["user"]),
        ("13. Depolama Durumunu GB Cinsinden Göster", storage_status, ICONS["disk"]),
        ("14. Sabit Diski Tara", scan_disk, ICONS["tools"]),
        ("15. Store Uygulamalarını Güncelle", update_store, ICONS["update"]),
        ("16. DNS Önbelleğini Temizle", flush_dns, ICONS["network"]),
        ("17. Sistem Dosyalarını Onar", repair_sfc, ICONS["tools"]),
        ("18. Disk Temizliği", disk_cleanup, ICONS["disk"]),
        ("19. Tüm Programları Güncelle", update_all, ICONS["update"]),
        ("20. Güvenlik Duvarını Kapat", firewall_off, ICONS["firewall"]),
        ("21. Güvenlik Duvarını Aç", firewall_on, ICONS["firewall"]),
        ("22. Gereksiz Dosyaları Temizle", clean_temp, ICONS["tools"]),
        ("23. RAM Optimizasyonu Yap", optimize_ram, ICONS["ram"]),
        ("24. Ping Testi Yap", ping_test, ICONS["network"]),
        ("25. Tracert Yap", tracert_test, ICONS["network"]),
        ("26. Nslookup Yap", nslookup_test, ICONS["network"]),
        ("27. Netstat Göster", netstat, ICONS["network"]),
        ("28. ARP Tablosunu Göster", arp, ICONS["network"]),
        ("29. Route Göster", route, ICONS["network"]),
        ("30. Sistem Bilgilerini Göster", sys_info, ICONS["system"]),
        ("31. IP Yapılandırmasını Göster", ip_config, ICONS["network"]),
        ("32. IP'yi Serbest Bırak", release_ip, ICONS["network"]),
        ("33. IP'yi Yenile", renew_ip, ICONS["network"]),
        ("34. Windows Sürüm Bilgisi", win_version, ICONS["info"]),
        ("35. Çık", root.quit, ICONS["exit"]),
    ]

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
            padx=15,
        )
        btn.grid(row=row, column=col, padx=15, pady=10, sticky="ew")
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    for i in range(3):
        frame.grid_columnconfigure(i, weight=1)

    root.mainloop()

if __name__ == "__main__":
    gui_main()
