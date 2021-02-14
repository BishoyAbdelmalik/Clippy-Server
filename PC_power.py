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
    sleep_cmd="Add-Type -Assembly System.Windows.Forms && [System.Windows.Forms.Application]::SetSuspendState( [System.Windows.Forms.PowerState]::Suspend, $fasle, $fasle);"
    os.system("powershell "+sleep_cmd)
def hibrnate():
    if theOS=="windows":
        os.system("shutdown /h")
    elif theOS=="linux":
        pass
    elif theOS=="darwin":
        pass