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
        webbrowser.open("http://localhost:"+str(flask_port)+"/static/qrcode.jpg")

    def close(icon, item):
        global pid
        os.kill(pid,0)
        os._exit(0)
    close_item=item(
                'Close',
                close,
                checked=None)
    open_interface=item(
                'Open',
                open_interface,
                checked=None)
    menu=menu(open_interface,close_item)
    # Update the state in `on_clicked` and return the new state in
    # a `checked` callable
    system_icon =icon('Clippy', Image.open("py.png"), menu=menu).run()