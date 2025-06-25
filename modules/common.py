# modules/common.py
import subprocess
import ctypes

def get_oem_encoding():
    """
    Windows OEM code page döner, örneğin 'cp850' veya 'cp857'.
    Başarısız olursa None döner.
    """
    try:
        cp = ctypes.windll.kernel32.GetOEMCP()
        return f"cp{cp}"
    except Exception:
        return None

def run_cmd(cmd_list, use_powershell=False):
    """
    Komutu çalıştırır, stdout ve stderr'ü bytes olarak alıp decode eder.
    - cmd_list: 
      * use_powershell=False iken: liste halinde komut ve argümanlar, örn. ["ipconfig","/all"]
      * use_powershell=True iken: cmd_list bir str: PowerShell komut dizgesi, örn. "Get-ComputerInfo | Select CsName"
    - use_powershell: True ise ["powershell","-Command", cmd_list] şeklinde çağrılır.
    Decode aşamasında önce OEM kod sayfasını dener; hata olursa fallback ile errors='replace' kullanır.
    Döner: (returncode, stdout_str, stderr_str)
    """
    encoding = get_oem_encoding()  # örn. 'cp857'
    try:
        if use_powershell:
            popen_args = ["powershell", "-Command", cmd_list]
        else:
            popen_args = cmd_list  # liste halinde

        proc = subprocess.Popen(popen_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_bytes, err_bytes = proc.communicate()
        # Decode:
        if encoding:
            try:
                out = out_bytes.decode(encoding, errors='replace')
                err = err_bytes.decode(encoding, errors='replace')
            except Exception:
                out = out_bytes.decode(errors='replace')
                err = err_bytes.decode(errors='replace')
        else:
            out = out_bytes.decode(errors='replace')
            err = err_bytes.decode(errors='replace')
        return proc.returncode, out.strip(), err.strip()
    except Exception as e:
        return -1, "", f"run_cmd exception: {e}"

def run_powershell(cmd):
    """
    PowerShell komutunu çalıştırmak için wrapper.
    cmd: PowerShell komut dizgesi, örn. "Get-ComputerInfo | Select CsName"
    """
    return run_cmd(cmd, use_powershell=True)

def pause():
    """
    Ekranda çıktı gösterildikten sonra kullanıcı Enter’a basana kadar bekler.
    """
    input("\nDevam etmek için Enter’a basın...")
