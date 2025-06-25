# 🛠 IT Hızlı Araç Kiti | Windows & Linux Destekli Sistem Yardımcı Aracı

## 📌 Proje Tanımı

**IT Hızlı Araç Kiti**, Windows ve Linux sistemleri için geliştirilmiş, sistem yöneticilerine yönelik çok amaçlı bir araçtır. Sistemsel bilgilerin görüntülenmesi, ağ analizi, disk taramaları, yazılım güncellemeleri gibi bir dizi günlük görevleri kullanıcı dostu bir grafik arayüz üzerinden gerçekleştirmeye olanak tanır.

Proje, Python dili ile geliştirilmiştir ve platform bağımsız çalışabilir şekilde yapılandırılmıştır. Windows ve Kali Linux ortamlarında denenmiş ve optimize edilmiştir.

---

## 🖥 Platform Desteği

| İşletim Sistemi | Destek Durumu | Test Edilen Sürümler |
|-----------------|----------------|-----------------------|
| Windows         | ✅ Tam destek   | Windows 10, 11        |
| Kali Linux      | ✅ Tam destek   | Kali 2023.4, 2024.1   |
| Diğer Linux'lar | 🔄 Kısmi destek | Ubuntu 22.04 (test edilmeli) |

---

## ⚙️ Özellikler

### ✅ Windows Özellikleri

- Grup politikası güncelleme
- IP yapılandırması gösterimi
- Lisans bilgisi (Product Key son 5 karakter)
- Wi-Fi şifrelerini listeleme (profil üzerinden)
- Disk durumu tarama (`chkdsk`)
- Windows sürüm, CPU, RAM, disk, kullanıcı, model bilgisi alma
- DNS temizleme, sistem dosyası kontrolü (`sfc`)
- Güvenlik duvarı açma / kapatma
- Gereksiz dosya temizliği
- Store uygulamalarını güncelleme
- Ping, Tracert, Nslookup, Netstat, ARP, Route testleri
- Tüm işlemler log dosyasına (`JSON`) kaydedilir

### ✅ Linux Özellikleri

- Sistem Bilgisi (hostname, uptime, kernel, CPU, RAM, disk, GPU vs.)
- Ağ Bilgileri (IP adresleri, gateway, DNS, traceroute, ping)
- Port Dinleme Bilgisi (netstat, ss)
- Paket güncelleme (`apt upgrade`, `apt list`)
- Hedefe ping, traceroute
- Sistem yükü ve disk kullanımı raporu
- JSON loglama özelliği (Linux versiyonunda da dahil)
- Gelişmiş hata yönetimi

---

## 🛠 Kurulum

### 📦 Bağımlılıklar

- Python 3.8+
- `tkinter` (çoğu sistemde varsayılan gelir)
- Windows için: `runas` yetkileri
- Linux için: `sudo` gereklidir

### 🔧 Kurulum Adımları

```bash
# Projeyi klonla
git clone https://github.com/kullaniciadi/it-hizli-arac-kiti.git
cd it-hizli-arac-kiti

# Windows
python main_windows.py

# Linux
python3 main_linux.py
