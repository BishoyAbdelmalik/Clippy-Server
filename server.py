# WS server example

import asyncio
from notification import send_email_toast, send_email_toast
import websockets
import logging
import pyperclip
import json
import platform
from subprocess import Popen, PIPE
import signal
import qrcode as qr
import webbrowser
import validators
import logger
import os
import sys
from helper import get_my_ip_address, is_port_in_use, create_dir_if_missing,get_flask_port_when_up

# Set up logging
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)
create_dir_if_missing("logs")
clippy_logger = logging.getLogger("clippy_logger")
clippy_logger.addHandler(logger.SQLiteHandler("logs/websocket.db","logs"))

try:
    import pyautogui
    from notification import send_link_toast
except:
    clippy_logger.warning("Not running on Windows, probably.")

from PC_power import hibrnate, reboot, shutdown, sleep 

create_dir_if_missing("config")
# maybe use below to start flask
flask_process = Popen([sys.executable, 'flaskserver.py'],stdout=PIPE)
print("Flask PID "+str(flask_process.pid))

ip = get_my_ip_address()
port = 8765
config_path="config/websocket.json"
if os.path.exists(config_path):
    loaded_machine_info=json.load(open(config_path,"r"))
    port = loaded_machine_info["port"]
        
# change port if port taken 
while is_port_in_use(port):
    port=port+1
    
machine_info = {"ip" : ip, "port" : port}
machine_info_json=json.dumps(machine_info)
with open(config_path,"w") as f:
    print(machine_info_json,file=f)
    f.close()
flask_port=get_flask_port_when_up("config/flask.json")
clippy_logger.info(f"Running with IP {ip} on port {port}")
clippy_logger.info(f"Flask Running with IP {ip} on port {flask_port}")

machine_info_json=json.dumps({"ip" : ip, "port" : port,"flask_port":flask_port})

qrcode = qr.make(machine_info_json)
try:
    # TODO: Figure out why this doesn't work on Linux
    qrcode.save("./static/qrcode.jpg")
except:
    clippy_logger.error(f"QR code machine broke")

# get os and save it
theOS=platform.system().lower()

# webbrowser.open("http://localhost:"+str(flask_port)+"/static/qrcode.jpg")
def take_screenshot() -> str:
    folder='upload'
    create_dir_if_missing(folder)
    path=folder+'\\my_screenshot.png'
    pyautogui.screenshot(path)
    return os.getcwd()+"\\"+path
async def send_to_client(websocket,msg:dict)->None:
    if not isinstance(msg,dict):
        raise TypeError("msg need to be a dict") 
    else:
        msg_str=json.dumps(msg)
        clippy_logger.info(f"> {msg_str}")
        await websocket.send(msg_str)

async def get_from_client(websocket)->dict:
    msg =await websocket.recv()
    clippy_logger.info(f"< {msg}")
    return json.loads(msg)

def mouse_input(command : str) -> None:
    if command=="click":
        pyautogui.click() 
    elif command=="right_click":
        pyautogui.click(button='right')
    elif command.startswith("scroll"):
         scroll_distance=command.split(",")[1]
         pyautogui.scroll(int(scroll_distance))
    elif command=="up":
        # TODO make this use numerical input
         pyautogui.moveTo(pyautogui.position().x,pyautogui.position().y-10)
    elif command=="down":
         pyautogui.moveTo(pyautogui.position().x,pyautogui.position().y+10)
    elif command=="left":
         pyautogui.moveTo(pyautogui.position().x-10,pyautogui.position().y)
    elif command=="right":
         pyautogui.moveTo(pyautogui.position().x+10,pyautogui.position().y)
    else:
        distance=command.split(",")
        pyautogui.move(float(distance[0]),float(distance[1]))
def keyboard_input(command : str) -> None:
    if command.startswith("hotkey"):
        keys=command.split(",")[1:]
        for k in keys:
            pyautogui.keyDown(k)
        for k in reversed(keys):
            pyautogui.keyUp(k)
    elif command == "browseropen":
        webbrowser.open_new("http://localhost:"+str(flask_port))
    else:
        pyautogui.press(command)
    
         
def execute_commands(command : str) -> None:
    if command=="playPause":
        pyautogui.press(command.lower())
    if command=="volumeUp":
        pyautogui.press(command.lower())
    if command=="volumeDown":
        pyautogui.press(command.lower())
    if command=="volumeMute":
        pyautogui.press(command.lower())
    if command=="shutdown":
        shutdown()
    if command=="reboot":
        reboot()
    if command=="sleep":
        sleep()
    if command=="hibernate":
        hibrnate()
    else:
        pass
    pass

def open_links(msg:str)->None:
    words=msg.split()
    for w in words:
        if validators.url(w):
            send_link_toast(w)
def emails_notification(msg:str)->None:
    words=msg.split()
    for w in words:
        if validators.email(w):
            send_email_toast(w)
        elif validators.email(w[1:len(w)-1]):
            send_email_toast(w[1:len(w)-1])
clipboard_data=""
file_path=[]
async def mysocket(websocket, path:str)->None:
    global clipboard_data
    global theOS
    global file_path
    playing=None
    client=websocket.remote_address[0]
    clippy_logger.info(client + " connected")
    if client==ip:
        clippy_logger.info("localhost connected")
    # what the client sends to the server
    if path[1:] == "send":   
        msg = await get_from_client(websocket)
        if msg["type"] == "clipboard":
            clipboard_data=msg["data"]
            pyperclip.copy(clipboard_data)
            open_links(clipboard_data)
            emails_notification(clipboard_data)
        elif msg["type"]=="command":
            execute_commands(msg["data"])
        elif msg["type"]=="info_send_file":
            file_path.append(msg["data"])
        elif msg["type"]=="get_screenshot":
            screenshot_path=take_screenshot()
            msg={"type":"file_screenshot","data":screenshot_path}
            await send_to_client(websocket,msg)
        elif msg["type"]=="mouse_input" or msg["type"]=="keyboard_input":
            while True:
                if msg["type"]=="mouse_input":
                    mouse_input(msg["data"])
                elif  msg["type"]=="keyboard_input":
                    keyboard_input(msg["data"])
                msg = await get_from_client(websocket)
        elif msg["type"]=="PC_name":
            if msg["data"] != platform.node():
                msg={"type":"PC_name","data":platform.node()}
                await send_to_client(websocket,msg)            
        else:
            pass
        # await websockets.protocol.WebSocketCommonProtocol.close(1000,"no reason")
        return
    if path[1:]=="get":
        msg={"type":"PC_name","data":platform.node()}
        await send_to_client(websocket,msg)   
        clipboard_data=""
    file_sent=""
    # what the server sends to the client
    while True and path[1:] == "get":
        try:
            if not clipboard_data==pyperclip.paste():
                clipboard_data=pyperclip.paste()
                if str(clipboard_data).strip() !="":
                    msg={"type":"clipboard","data":clipboard_data}
                    await send_to_client(websocket,msg)
        except Exception as e:
            print(e)
            
        if not file_path==[]:
            file_sent=file_path.pop()
            msg={"type":"file_path","data":file_sent}
            await send_to_client(websocket,msg)
        if theOS=="windows":
            # get whats playing
            playing_process = Popen([sys.executable, 'current_playing.py'],stdout=PIPE)
            out, err = playing_process.communicate()
            # print(out)
            playingNow=json.loads(out)
            # playingNow=await current_playing.get_media_info()
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

icon = Popen([sys.executable, 'system_tray.py',str(os.getpid()),str(flask_port)],stdout=PIPE)

start_server = websockets.serve(mysocket, host=None,port=port)
logger = logging.getLogger('websockets.server')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
