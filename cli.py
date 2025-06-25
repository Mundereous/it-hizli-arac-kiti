import os
import sys
import ctypes
from modules.common import run_cmd, run_powershell, pause


def is_admin():
    """
    Yönetici olarak çalıştırıldığını kontrol eder.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def main():
    # Yönetici kontrolü
    if not is_admin():
        print("UYARI: Bu program yönetici haklarıyla çalışmıyor. Bazı işlemler başarısız olabilir.")
        print("Lütfen Komut İstemi veya PowerShell'i yönetici olarak açıp tekrar deneyin.")
        pause()
    while True:
        os.system("cls")
        print("=== IT Hızlı Araç Kiti - Windows ===")
        print("1.  Grup Politikalarını Güncelle (gpupdate /force)")
        print("2.  IP Göster")
        print("3.  Windows Lisans Göster")
        print("4.  Nbtstat Göster")
        print("5.  Wi-Fi Şifresini Göster")
        print("6.  Son Format Tarihini Göster")
        print("7.  Disk Durumunu Kontrol Et")
        print("8.  Windows Güncelleme Durumunu Göster")
        print("9.  CPU Bilgilerini Göster")
        print("10. Bellek (RAM) Kullanımını Göster")
        print("11. Bilgisayar Seri Numarasını, Adını, Marka ve Modelini Göster")
        print("12. Kullanıcı Hesaplarını Listele")
        print("13. Depolama Alanı Durumunu Göster")
        print("14. Sabit Diski Tarama")
        print("15. Windows Store Uygulamalarını Güncelle")
        print("16. Network DNS Önbelleğini Temizle")
        print("17. Windows Sistem Dosyalarını Onar")
        print("18. Disk Temizliği Başlat")
        print("19. Tüm Programları Güncelle")
        print("20. Güvenlik Duvarını Kapat")
        print("21. Güvenlik Duvarını Aç")
        print("22. Gereksiz Dosyaları Temizle")
        print("23. RAM Optimizasyonu Yap")
        print("24. Ping Testi Yap")
        print("25. Tracert Yap")
        print("26. Nslookup Yap")
        print("27. Netstat Göster")
        print("28. ARP Tablosunu Göster")
        print("29. Route Göster")
        print("30. Sistem Bilgilerini Görüntüle")
        print("31. IP Yapılandırmasını Görüntüle")
        print("32. IP Yapılandırmasını Serbest Bırak")
        print("33. IP Yapılandırmasını Yenile")
        print("34. Windows Sürüm Bilgisi")
        print("35. Çık")
        choice = input("Seçiminiz (1-35): ").strip()
        if choice == "1":
            gpupdate()
        elif choice == "2":
            show_ip()
        elif choice == "3":
            show_windows_license()
        elif choice == "4":
            nbtstat_show()
        elif choice == "5":
            show_wifi_passwords()
        elif choice == "6":
            show_last_format_date()
        elif choice == "7":
            check_disk_status()
        elif choice == "8":
            show_windows_update_status()
        elif choice == "9":
            show_cpu_info()
        elif choice == "10":
            show_ram_usage()
        elif choice == "11":
            show_computer_serial_model()
        elif choice == "12":
            list_user_accounts()
        elif choice == "13":
            show_storage_status()
        elif choice == "14":
            scan_disk()
        elif choice == "15":
            update_store_apps()
        elif choice == "16":
            clear_dns_cache()
        elif choice == "17":
            repair_system_files()
        elif choice == "18":
            start_disk_cleanup()
        elif choice == "19":
            update_all_programs()
        elif choice == "20":
            firewall_off()
        elif choice == "21":
            firewall_on()
        elif choice == "22":
            clean_unnecessary_files()
        elif choice == "23":
            optimize_ram()
        elif choice == "24":
            ping_test()
        elif choice == "25":
            tracert_test()
        elif choice == "26":
            nslookup_test()
        elif choice == "27":
            show_netstat()
        elif choice == "28":
            show_arp_table()
        elif choice == "29":
            show_route()
        elif choice == "30":
            show_system_info()
        elif choice == "31":
            show_ip_config()
        elif choice == "32":
            release_ip()
        elif choice == "33":
            renew_ip()
        elif choice == "34":
            show_windows_version()
        elif choice == "35":
            print("Programdan çıkılıyor...")
            break
        else:
            print("Geçersiz seçim.")
            pause()


def gpupdate():
    print("\nGrup Politikaları güncelleniyor (gpupdate /force)...")
    code, out, err = run_cmd(["gpupdate", "/force"] )
    if code == 0:
        print(out)
    else:
        print("Hata:", err)
    pause()


def show_ip():
    print("\nIP konfigürasyonu alınıyor (ipconfig /all)...")
    code, out, err = run_cmd(["ipconfig", "/all"] )
    if code == 0:
        print(out)
    else:
        print("Hata:")
        print(err)
    pause()


def show_windows_license():
    print("\nWindows lisans bilgisi alınıyor (slmgr /dlv)...")
    # slmgr genellikle GUI dialog açabilir; komut satırı çıktısı olmayabilir.
    code, out, err = run_cmd(["slmgr", "/dlv"])
    if code == 0:
        print(out)
    else:
        print("Hata:", err)
    pause()


def nbtstat_show():
    print("\nNBTSTAT bilgisi alınıyor (nbtstat -n)...")
    code, out, err = run_cmd(["nbtstat", "-n"] )
    if code == 0:
        print(out)
    else:
        print("Hata:", err)
    pause()


def show_wifi_passwords():
    print("\nWi-Fi profilleri ve şifreleri alınıyor...")
    code, out, err = run_cmd("netsh wlan show profiles", use_powershell=True)
    if code != 0:
        print("Hata profilleri alırken:", err)
        pause()
        return
    print("Kayıtlı Profiller:")
    print(out)
    # Profilleri ayıkla
    profiles = []
    for line in out.splitlines():
        line = line.strip()
        if line.lower().startswith("all user profile"):
            parts = line.split(":", 1)
            if len(parts) == 2:
                profil = parts[1].strip()
                profiles.append(profil)
    if not profiles:
        print("Hiç Wi-Fi profili bulunamadı.")
        pause()
        return
    for profil in profiles:
        print(f"\nProfil: {profil}")
        cmd = f'netsh wlan show profile name="{profil}" key=clear'
        code2, out2, err2 = run_cmd(cmd, use_powershell=True)
        if code2 != 0:
            print(f"Hata şifreyi alırken ({profil}):", err2)
        else:
            pwd = None
            for line2 in out2.splitlines():
                line2 = line2.strip()
                if line2.lower().startswith("key content"):
                    parts2 = line2.split(":", 1)
                    if len(parts2) == 2:
                        pwd = parts2[1].strip()
                        break
            if pwd:
                print("  Şifre:", pwd)
            else:
                print("  Şifre bulunamadı veya kaydedilmemiş.")
    pause()


def show_last_format_date():
    print("\nSon format tarihi gösterimi (yaklaşık)...")
    try:
        attrs = os.stat(r"C:\Windows")
        import datetime
        ts = attrs.st_ctime
        dt = datetime.datetime.fromtimestamp(ts)
        print("C:\\Windows klasörünün oluşturulma zamanı (sistem kurulumu tahmini):", dt)
    except Exception as e:
        print("Hata:", e)
    pause()


def check_disk_status():
    print("\nDisk durumu (chkdsk C: /scan) kontrol ediliyor...")
    code, out, err = run_cmd("chkdsk C: /scan", use_powershell=True)
    if code == 0:
        print(out)
    else:
        print("Hata:", err)
    pause()


def show_windows_update_status():
    print("\nWindows Update durumu alınıyor...")
    print("Bu özellik için PSWindowsUpdate modülü gerekebilir.")
    pause()


def show_cpu_info():
    print("\nCPU bilgileri alınıyor (Get-CimInstance)...")
    # Daha güncel Get-CimInstance örneği
    cmd = "Get-CimInstance Win32_Processor | Select Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed"
    code, out, err = run_cmd(cmd, use_powershell=True)
    if code != 0:
        print("Hata:", err)
        pause()
        return
    # Parse
    info = {}
    for line in out.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            info[k.strip()] = v.strip()
    name = info.get("Name", "Bilinmiyor")
    cores = info.get("NumberOfCores", "Bilinmiyor")
    threads = info.get("NumberOfLogicalProcessors", "Bilinmiyor")
    speed = info.get("MaxClockSpeed", "Bilinmiyor")
    print(f"CPU Adı: {name}")
    print(f"Çekirdek Sayısı: {cores}")
    print(f"Mantıksal İş Parçacığı: {threads}")
    print(f"Maksimum Saat Hızı: {speed} MHz")
    pause()


def show_ram_usage():
    print("\nBellek (RAM) kullanım bilgisi alınıyor...")
    cmd = "Get-CimInstance Win32_OperatingSystem | Select TotalVisibleMemorySize,FreePhysicalMemory"
    code, out, err = run_cmd(cmd, use_powershell=True)
    if code != 0:
        print("Hata:", err)
        pause()
        return
    # Parse KB -> MB
    info = {}
    for line in out.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            info[k.strip()] = v.strip()
    total_kb = int(info.get("TotalVisibleMemorySize", 0))
    free_kb = int(info.get("FreePhysicalMemory", 0))
    total_mb = total_kb / 1024
    free_mb = free_kb / 1024
    used_mb = total_mb - free_mb
    print(f"Toplam Bellek: {total_mb:.2f} MB")
    print(f"Kullanılan Bellek: {used_mb:.2f} MB")
    print(f"Boş Bellek: {free_mb:.2f} MB")
    pause()


def show_computer_serial_model():
    print("\nBilgisayar seri numarası, marka, model alınıyor...")
    code, out, err = run_cmd("Get-CimInstance Win32_BIOS | Select SerialNumber", use_powershell=True)
    if code == 0:
        print("Serial Number:")
        print(out)
    else:
        print("Hata:", err)
    code2, out2, err2 = run_cmd("Get-CimInstance Win32_ComputerSystem | Select Manufacturer,Model,Name", use_powershell=True)
    if code2 == 0:
        print("Manufacturer ve Model ve Name:")
        print(out2)
    else:
        print("Hata:", err2)
    pause()


def list_user_accounts():
    print("\nKullanıcı hesapları listeleniyor...")
    cmd = "Get-CimInstance Win32_UserAccount | Where-Object {$_.LocalAccount -eq $true} | Select Name,FullName,Disabled"
    code, out, err = run_cmd(cmd, use_powershell=True)
    if code == 0:
        print(out)
    else:
        print("Hata:", err)
    pause()


def show_storage_status():
    print("\nDepolama alanı bilgisi alınıyor...")
    cmd = "Get-CimInstance Win32_LogicalDisk | Select DeviceID,Size,FreeSpace"
    code, out, err = run_cmd(cmd, use_powershell=True)
    if code != 0:
        print("Hata:", err)
        pause()
        return
    # Parse ve GB cinsine dönüştür
    for line in out.splitlines():
        if ":" in line:
            # Basit parse yapı: satır satır değil, isterseniz ayrıştırma derinleştirin
            print(line)
    pause()


def scan_disk():
    print("\nSabit diski tarama (chkdsk)...")
    scan = input("Sürücü harfi girin (örn. C): ").strip().upper()
    if len(scan) == 1 and scan.isalpha():
        cmd = f"chkdsk {scan}: /scan"
        code, out, err = run_cmd(cmd, use_powershell=True)
        if code == 0:
            print(out)
        else:
            print("Hata:", err)
    else:
        print("Geçersiz sürücü harfi.")
    pause()


def update_store_apps():
    print("\nWindows Store uygulamalarını güncelleme (yeniden kaydet)...")
    cmd = "Get-AppxPackage -AllUsers | Foreach { Add-AppxPackage -DisableDevelopmentMode -Register \"$($_.InstallLocation)\\AppXManifest.xml\" }"
    code, out, err = run_cmd(cmd, use_powershell=True)
    if code == 0:
        print("Komut çalıştırıldı, sonuç:")
        print(out)
    else:
        print("Hata:", err)
    pause()


def clear_dns_cache():
    print("\nDNS önbelleği temizleniyor (ipconfig /flushdns)...")
    code, out, err = run_cmd(["ipconfig", "/flushdns"])
    if code == 0:
        print(out)
    else:
        print("Hata:", err)
    pause()


def repair_system_files():
    print("\nSistem dosyaları onarılıyor (sfc /scannow)...")
    code, out, err = run_cmd(["sfc", "/scannow"])
    if code == 0:
        print(out)
    else:
        print("Hata veya uyarı:", out or err)
    pause()


def start_disk_cleanup():
    print("\nDisk temizleme aracı başlatılıyor (cleanmgr)...")
    # GUI açar
    os.system("cleanmgr")
    pause()


def update_all_programs():
    print("\nTüm programları güncelleme (winget)...")
    code, out, err = run_cmd(["winget", "upgrade", "--all", "--silent"] )
    if code == 0:
        print(out)
    else:
        print("Hata veya Winget yüklü değil olabilir:")
        print(err)
    pause()


def firewall_off():
    print("\nWindows Güvenlik Duvarı kapatılıyor...")
    code, out, err = run_cmd("Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False", use_powershell=True)
    if code == 0:
        print("Güvenlik duvarı profilleri kapatıldı.")
    else:
        print("Hata:", err)
    pause()


def firewall_on():
    print("\nWindows Güvenlik Duvarı açılıyor...")
    code, out, err = run_cmd("Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True", use_powershell=True)
    if code == 0:
        print("Güvenlik duvarı profilleri açıldı.")
    else:
        print("Hata:", err)
    pause()


def clean_unnecessary_files():
    print("\nGereksiz dosyaları temizleme (kullanıcı TEMP)...")
    temp = os.environ.get("TEMP")
    if temp:
        print("Temp klasörü:", temp)
        confirm = input("Bu klasördeki 7 günden eski dosyaları silmek istiyor musunuz? (E/h): ").strip().lower()
        if confirm == "e":
            import time, shutil
            now = time.time()
            cutoff = now - 7*86400
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
            print(f"Silinen öğe sayısı (yaklaşık): {deleted}")
        else:
            print("İptal edildi.")
    else:
        print("TEMP ortam değişkeni bulunamadı.")
    pause()


def optimize_ram():
    print("\nRAM optimizasyonu: Windows kendi yönetimini yapar; manuel komut önerilmez.")
    pause()


def ping_test():
    host = input("Ping yapmak istediğiniz adresi yazın (örn. 8.8.8.8): ").strip()
    if host:
        code, out, err = run_cmd(["ping", "-n", "4", host])
        if code == 0:
            print(out)
        else:
            print("Hata:")
            print(err)
    else:
        print("Geçersiz adres.")
    pause()


def tracert_test():
    host = input("Trace route için adres yazın (örn. google.com): ").strip()
    if host:
        code, out, err = run_cmd(["tracert", host])
        if code == 0:
            print(out)
        else:
            print("Hata:")
            print(err)
    else:
        print("Geçersiz adres.")
    pause()


def nslookup_test():
    host = input("Nslookup için adres yazın (örn. google.com): ").strip()
    if host:
        code, out, err = run_cmd(["nslookup", host])
        if code == 0:
            print(out)
        else:
            print("Hata:")
            print(err)
    else:
        print("Geçersiz adres.")
    pause()


def show_netstat():
    print("\nNetstat bilgisi alınıyor (netstat -ano)...")
    code, out, err = run_cmd(["netstat", "-ano"] )
    if code == 0:
        print(out)
    else:
        print("Hata:", err)
    pause()


def show_arp_table():
    print("\nARP tablosu alınıyor (arp -a)...")
    code, out, err = run_cmd(["arp", "-a"] )
    if code == 0:
        print(out)
    else:
        print("Hata:", err)
    pause()


def show_route():
    print("\nRoute tablosu alınıyor (route print)...")
    code, out, err = run_cmd(["route", "print"] )
    if code == 0:
        print(out)
    else:
        print("Hata:", err)
    pause()


def show_system_info():
    print("\nSistem bilgisi alınıyor (PowerShell Get-ComputerInfo)...")
    code, out, err = run_powershell("Get-ComputerInfo | Select CsName,OsName,OsVersion,OsArchitecture,OsBuildNumber")
    if code == 0:
        print(out)
    else:
        print("Hata:")
        print(err)
    pause()


def show_ip_config():
    print("\nIP yapılandırması alınıyor (ipconfig /all)...")
    code, out, err = run_cmd(["ipconfig", "/all"] )
    if code == 0:
        print(out)
    else:
        print("Hata:")
        print(err)
    pause()


def release_ip():
    print("\nIP yapılandırması serbest bırakılıyor (ipconfig /release)...")
    code, out, err = run_cmd(["ipconfig", "/release"] )
    if code == 0:
        print(out)
    else:
        print("Hata:")
        print(err)
    pause()


def renew_ip():
    print("\nIP yapılandırması yenileniyor (ipconfig /renew)...")
    code, out, err = run_cmd(["ipconfig", "/renew"] )
    if code == 0:
        print(out)
    else:
        print("Hata:")
        print(err)
    pause()


def show_windows_version():
    print("\nWindows sürüm bilgisi alınıyor...")
    code, out, err = run_powershell("Get-ComputerInfo | Select WindowsVersion,WindowsBuildLabEx")
    if code == 0:
        print(out)
    else:
        completed = run_cmd(["ver"])
        if completed[0] == 0:
            print(completed[1])
        else:
            print("Hata:", err or completed[2])
    pause()


if __name__ == "__main__":
    main()
