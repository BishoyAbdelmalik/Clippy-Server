import os
import platform
theOS=platform.system().lower()

def reboot():
    os.system("powershell Restart-Computer")
    # if theOS=="windows":
    #     # os.system("shutdown /r /t 0")
    # elif theOS=="linux":
    #     pass
    # elif theOS=="darwin":
    #     pass
def shutdown():
    os.system("powershell Stop-Computer")
    # if theOS=="windows":
    #     # os.system("shutdown /s /t 0")
    # elif theOS=="linux":
    #     pass
    # elif theOS=="darwin":
    #     pass
def sleep():
    if theOS=="windows":
        sleep_cmd="rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
    os.system("powershell "+sleep_cmd)
def hibrnate():
    if theOS=="windows":
        os.system("shutdown /h")
    elif theOS=="linux":
        pass
    elif theOS=="darwin":
        pass