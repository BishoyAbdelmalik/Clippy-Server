# WS server example

import asyncio
import websockets
import logging
import pyperclip
import json
import pyautogui
import platform
import current_playing
from subprocess import Popen, PIPE
import signal
import socket
import qrcode as qr
import webbrowser
import validators
from notification import send_link_toast
def get_my_ip_address(remote_server="google.com"):
    """
    Return the/a network-facing IP number for this system.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s: 
        s.connect((remote_server, 80))
        return s.getsockname()[0]
ip=get_my_ip_address()
port=8765
machine_info={"ip":ip,"port":port}
machine_info_json=json.dumps(machine_info)
print(machine_info_json)
qrcode = qr.make(machine_info_json)
qrcode.save("./static/qrcode.jpg")
# get os and save it
theOS=platform.system().lower()

# maybe use below to start flask
process = Popen(['python3', 'flaskserver.py'], stdout=PIPE, stderr=PIPE)
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
def execute_commands(command:str)->None:
    if command=="playPause":
        pyautogui.press("playpause")
    if command=="volumeUp":
        pyautogui.press("volumeup")
    if command=="volumeDown":
        pyautogui.press("volumedown")
    if command=="volumeMute":
        pyautogui.press("volumemute")
    else:
        pass
    pass
def open_links(msg:str)->None:
    words=msg.split()
    for w in words:
        if validators.url(w):
            send_link_toast(w)

clipboard_data=""
async def mysocket(websocket:websockets.server.WebSocketServerProtocol, path:str)->None:
    global clipboard_data
    global theOS
    playing=None
    print(websocket.remote_address[0]+" connected")
    # what the client sends to the server
    if path[1:] == "send":   
        msg = await get_from_client(websocket)
        if msg["type"] == "clipboard":
            clipboard_data=msg["data"]
            pyperclip.copy(clipboard_data)
            open_links(clipboard_data)
        elif msg["type"]=="command":
            execute_commands(msg["data"])
        else:
            pass
        # await websockets.protocol.WebSocketCommonProtocol.close(1000,"no reason")
        return
    
    
    # what the server sends to the client
    while True and path[1:] == "get":
        if not clipboard_data==pyperclip.paste():
            clipboard_data=pyperclip.paste()
            msg={"type":"clipboard","data":clipboard_data}
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