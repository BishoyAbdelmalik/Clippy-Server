import os
import platform
theOS=platform.system().lower()

def reboot():
    if theOS=="windows":
        os.system("shutdown /r /t 0")
    elif theOS=="linux":
        pass
    elif theOS=="darwin":
        pass
def shutdown():
    if theOS=="windows":
        os.system("shutdown /s /t 0")
    elif theOS=="linux":
        pass
    elif theOS=="darwin":
        pass
