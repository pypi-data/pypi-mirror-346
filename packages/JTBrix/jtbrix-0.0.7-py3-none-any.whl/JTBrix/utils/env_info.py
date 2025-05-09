import os
import platform

def print_sys_info():
    print("System:", platform.system())       # 'Darwin' (macOS), 'Linux', 'Windows'
    print("Machine:", platform.machine())     # 'x86_64', 'arm64', etc.
    print("Platform:", platform.platform())   # Full platform info
    print("OS name:", os.name)                # 'posix', 'nt'

def detect_environment():
    try:
        import google.colab
        print("Running in Google Colab")
        system = "Google Colab"
    except ImportError:
        system_type = platform.system()
        if system_type == "Darwin":
            print("Running on macOS")
            system = "macOS"
        elif system_type == "Linux":
            print("Running on Linux")
            system = "Linux"
        elif system_type == "Windows":
            print("Running on Windows")
            system = "Windows"
        else:
            print("Unknown operating system")
            system = "Unknown"

    print_sys_info()
    return system
    


if __name__ == "__main__":
    detect_environment()