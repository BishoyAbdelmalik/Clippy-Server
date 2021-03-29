from pystray import Icon as icon, Menu as menu, MenuItem as item
import sys
import os
from PIL import Image
import webbrowser

if __name__ == "__main__":
    args=sys.argv
    pid=int(args[1])
    flask_port=int(args[2])
    def open_interface(icon, item):
        webbrowser.open("http://localhost:"+str(flask_port)+"/")
    def open_qr(icon, item):
        webbrowser.open("http://localhost:"+str(flask_port)+"/static/qrcode.jpg")

    def close(icon, item):
        global pid
        os.kill(pid,0)
        system_icon.stop()
    close_item=item('Close',close,checked=None)
    open_interface_item=item('Open',open_interface,checked=None)
    viewqrcode_item=item('View QR Code',open_qr,checked=None)
    menu=menu(open_interface_item,viewqrcode_item,close_item)

    system_icon = icon('Clippy', Image.open("py.png"), menu=menu)
    system_icon.run()