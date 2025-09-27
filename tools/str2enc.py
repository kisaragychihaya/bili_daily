import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
HASH_NAME = "SHA256"
IV_LENGTH = 16
ITERATION_COUNT = 65536
KEY_LENGTH = 32
def pad(s): return s + (IV_LENGTH - len(s) % IV_LENGTH) * chr(IV_LENGTH - len(s) % IV_LENGTH).encode()


def unpad(s): return s[0:-ord(s[-1:])]
def get_machine_id():
    import platform
    import hashlib

    def get_hardware_info():
        import subprocess
        import os

        SYS_PLATFORM = sys.platform

        if SYS_PLATFORM == "win32":
            import wmi

            wmic = wmi.WMI()

        info = {}

        if SYS_PLATFORM == "linux":
            try:
                with open("/etc/machine-id", "r") as f:
                    machine_id = f.read().strip()
                    if machine_id and not machine_id.isspace():
                        info["machine_id"] = machine_id
            except:
                pass
        try:
            # CPU信息
            if SYS_PLATFORM == "win32":
                cpu_info = wmic.Win32_Processor()[0].ProcessorId.strip()
            else:
                cpu_info = None
                try:
                    if SYS_PLATFORM == "darwin":
                        cpu_info = (
                            subprocess.check_output(
                                ["sysctl", "-n", "machdep.cpu.brand_string"]
                            )
                            .decode()
                            .strip()
                        )
                except:
                    pass

            if cpu_info:
                info["cpu"] = cpu_info

            # 主板信息
            if SYS_PLATFORM == "win32":
                try:
                    baseboard = wmic.Win32_BaseBoard()[0].SerialNumber.strip()
                    if (
                            baseboard
                            and not baseboard.isspace()
                            and "default string" not in baseboard.lower()
                    ):
                        info["baseboard"] = baseboard
                except Exception:
                    pass

            # 磁盘序列号
            if SYS_PLATFORM == "win32":
                try:
                    # 使用 wmi 模块获取磁盘序列号
                    try:
                        for disk in wmic.Win32_DiskDrive():
                            serial = getattr(disk, "SerialNumber", None)
                            if serial and not serial.isspace():
                                info["disk"] = serial.strip()
                                break
                    except Exception:
                        pass
                except:
                    pass
        except:
            pass

        return info

    # 获取硬件信息
    hardware_info = get_hardware_info()

    unique_data = {
        "hardware": hardware_info,
        "platform": platform.system(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }

    unique_str = str(unique_data).encode("utf-8")

    hash_obj = hashlib.sha256(unique_str)
    machine_code = hash_obj.digest()

    return machine_code
def str2enc(data:bytes|str) -> bytes:
    if isinstance(data, str):
        data = data.encode("utf-8")
    data=pad(data)
    password = get_machine_id()
    iv  = get_random_bytes(IV_LENGTH)  # iv偏移量，bytes类型
    aes = AES.new(password, AES.MODE_CBC, iv)  # 创建一个aes对象
    # AES.MODE_CBC 表示模式是CBC模式
    en_text = aes.encrypt(data)
    print("密文：", iv+en_text)  # 加密明文，bytes类型
    return iv+en_text

def enc2str(data:bytes) -> str:
    iv = data[:IV_LENGTH]
    cipher = AES.new(get_machine_id(), AES.MODE_CBC, iv)
    original_bytes = unpad(cipher.decrypt(data[IV_LENGTH:]))
    return bytes.decode(original_bytes)


if __name__ == "__main__":
    with open("../cookies.json", "r") as f:
        data=f.read()
        data=str2enc(data)
    with open("../cookies.json", "wb") as f:
        f.write(data)