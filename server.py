# WS server example

import asyncio
import websockets
import logging
import pyperclip
import json
import platform
from subprocess import Popen, PIPE
import signal
import socket
import qrcode as qr
import webbrowser
import validators

# Set up logging
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

clippy_logger = logging.getLogger("clippy_logger")

try:
    import current_playing
    import pyautogui
    from notification import send_link_toast
except:
    clippy_logger.warning("Not running on Windows, probably.")

from PC_power import hibrnate, reboot, shutdown, sleep 

def get_my_ip_address(remote_server="google.com"):
    """
    Return the/a network-facing IP number for this system.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s: 
        s.connect((remote_server, 80))
        return s.getsockname()[0]

ip = get_my_ip_address()
port = 8765
machine_info = {"ip" : ip, "port" : port}
machine_info_json=json.dumps(machine_info)
clippy_logger.info(f"Running with IP {ip} on port {port}")
qrcode = qr.make(machine_info_json)
try:
    # TODO: Figure out why this doesn't work on Linux
    qrcode.save("./static/qrcode.jpg")
except:
    clippy_logger.error(f"QR code machine broke")

# get os and save it
theOS=platform.system().lower()

# maybe use below to start flask
process = Popen(['python', 'flaskserver.py'], stdout=PIPE, stderr=PIPE)
# flask is blocking arian
# async def main():
#     from flaskserver import run_flask

#     app = run_flask()
#     app.run(debug=True,host= '0.0.0.0')
# asyncio.run(main())
webbrowser.open("http://localhost:5000/static/qrcode.jpg")

async def send_to_client(websocket:websockets.server.WebSocketServerProtocol,msg:dict)->None:
    if not isinstance(msg,dict):
        raise TypeError("msg need to be a dict") 
    else:
        msg_str=json.dumps(msg)
        print(f"> {msg_str}")
        await websocket.send(msg_str)

async def get_from_client(websocket:websockets.server.WebSocketServerProtocol)->dict:
    msg =await websocket.recv()
    print(f"< {msg}")
    return json.loads(msg)

def execute_commands(command : str) -> None:
    if command=="playPause":
        pyautogui.press("playpause")
    if command=="volumeUp":
        pyautogui.press("volumeup")
    if command=="volumeDown":
        pyautogui.press("volumedown")
    if command=="volumeMute":
        pyautogui.press("volumemute")
    if command=="shutdown":
        shutdown()
    if command=="reboot":
        reboot()
    if command=="sleep":
        sleep()
    if command=="hibrnate":
        hibrnate()
    else:
        pass
    pass

def open_links(msg:str)->None:
    words=msg.split()
    for w in words:
        if validators.url(w):
            send_link_toast(w)

clipboard_data=""
file_path=""
async def mysocket(websocket:websockets.server.WebSocketServerProtocol, path:str)->None:
    global clipboard_data
    global theOS
    global file_path
    playing=None
    client=websocket.remote_address[0]
    print(client+" connected")
    if client==ip:
        print("localhost connected")
    # what the client sends to the server
    if path[1:] == "send":   
        msg = await get_from_client(websocket)
        if msg["type"] == "clipboard":
            clipboard_data=msg["data"]
            pyperclip.copy(clipboard_data)
            open_links(clipboard_data)
        elif msg["type"]=="command":
            execute_commands(msg["data"])
        elif msg["type"]=="info_send_file":
            file_path=msg["data"]
        else:
            pass
        # await websockets.protocol.WebSocketCommonProtocol.close(1000,"no reason")
        return
    
    file_sent=""
    # what the server sends to the client
    while True and path[1:] == "get":
        if not clipboard_data==pyperclip.paste():
            clipboard_data=pyperclip.paste()
            msg={"type":"clipboard","data":clipboard_data}
            await send_to_client(websocket,msg)
        if not file_sent == file_path:
            file_sent=file_path
            file_path=""
            msg={"type":"file_path","data":file_sent}
            await send_to_client(websocket,msg)
        if theOS=="windows":
            # get whats playing
            playingNow=await current_playing.get_media_info()
            # check if we were playing but now we arent
            if playingNow==None and not playing==None:
                playing=={}
            # if we are playing something new
            if not playingNow==playing:
                playing=playingNow
                if not playing == None:
                    playingNowDict={"type":"media","title":playing["title"],"thumbnail":playing["thumbnail"]}    
                else:
                    playingNowDict={"type":"media","title":"Nothing Playing","thumbnail":""}
                msg={"type":"info","data":playingNowDict}
                await send_to_client(websocket,msg)
        elif theOS=="linux":
            pass
        elif theOS=="darwin":
            pass
        await asyncio.sleep(3)

start_server = websockets.serve(mysocket, host=None,port=port)
logger = logging.getLogger('websockets.server')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
