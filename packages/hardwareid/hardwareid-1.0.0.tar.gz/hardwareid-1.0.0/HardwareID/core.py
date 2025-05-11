import platform
import subprocess
import hashlib
import os

def is_wsl():
    """Определяем, запущены ли мы в Windows Subsystem for Linux (WSL)"""
    return platform.system() == "Linux" and "microsoft" in platform.release().lower()

def get_hwid_data():
    """Главная функция для получения идентификационных данных"""
    system = platform.system()
    
    if is_wsl():
        return generate_sha3_512(get_windows_data_via_ps())
    elif system == "Windows":
        return generate_sha3_512(get_windows_data_native())
    elif system == "Linux":
        return generate_sha3_512(get_linux_data())
    else:
        raise NotImplementedError(f"Unsupported OS: {system}")

def get_windows_data_via_ps():
    """Сбор данных через PowerShell для WSL"""
    ps_script = '''
    $baseboard = (Get-WmiObject Win32_BaseBoard).SerialNumber.Trim()
    $processor = (Get-WmiObject Win32_Processor).ProcessorId.Trim()
    $bios = (Get-WmiObject Win32_BIOS).SerialNumber.Trim()
    "$baseboard|$processor|$bios"
    '''
    
    try:
        result = subprocess.run(
            ["powershell.exe", "-Command", ps_script],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        return result.stdout.strip()
    except Exception as e:
        raise RuntimeError(f"PowerShell error: {str(e)}")

def get_windows_data_native():
    """Сбор данных через WMI для чистой Windows"""
    try:
        import wmi
        c = wmi.WMI()
        
        baseboard = c.Win32_BaseBoard()[0].SerialNumber.strip()
        processor = c.Win32_Processor()[0].ProcessorId.strip()
        bios = c.Win32_BIOS()[0].SerialNumber.strip()
        
        return f"{baseboard}|{processor}|{bios}"
    except Exception as e:
        raise RuntimeError(f"WMI error: {str(e)}")

def get_linux_data():
    """Сбор данных для Linux без использования sudo"""
    identifiers = []
    
    # 1. DMI данные из sysfs
    dmi_fields = ["board_serial", "product_uuid", "bios_serial"]
    identifiers += [read_dmi_file(field) for field in dmi_fields]
    
    # 2. Системный machine-id
    identifiers.append(get_linux_machine_id())
    
    # 3. Информация о процессоре
    identifiers.append(get_cpu_model())
    
    # 4. UUID корневого раздела
    identifiers.append(get_disk_uuid())
    
    return "|".join(filter(None, identifiers))

def read_dmi_file(field):
    """Чтение DMI данных из sysfs"""
    try:
        with open(f"/sys/class/dmi/id/{field}", "r") as f:
            return f.read().strip()
    except:
        return ""

def get_linux_machine_id():
    """Получение системного machine-id"""
    try:
        with open("/etc/machine-id", "r") as f:
            return f.read().strip()
    except:
        return ""

def get_cpu_model():
    """Получение модели процессора"""
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
            return ""
    except:
        return ""

def get_disk_uuid():
    """Получение UUID корневого раздела без sudo"""
    try:
        # Находим корневое устройство
        with open("/proc/mounts", "r") as f:
            for line in f:
                parts = line.split()
                if parts[1] == "/":
                    dev = parts[0]
                    break
            else:
                return ""
        
        # Ищем UUID в /dev/disk/by-uuid
        for uuid in os.listdir("/dev/disk/by-uuid"):
            dev_path = os.path.realpath(f"/dev/disk/by-uuid/{uuid}")
            if dev_path == dev:
                return uuid
        return ""
    except:
        return ""

def generate_sha3_512(data):
    """Генерация SHA3-512 хеша"""
    return hashlib.sha3_512(data.encode()).hexdigest()

