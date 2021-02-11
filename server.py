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

# get os and save it
theOS=platform.system().lower()

# process = Popen(['python3', 'flaskserver.py'], stdout=PIPE, stderr=PIPE)
async def send(websocket:websockets.server.WebSocketServerProtocol,msg:dict):
    if not isinstance(msg,dict):
        raise TypeError("msg need to be a dict") 
    else:
        msg=json.dumps(msg)
        print(f"> {msg}")
        await websocket.send(msg)
def execute_commands(command:str):
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
async def mysocket(websocket:websockets.server.WebSocketServerProtocol, path:str):
    content=""
    playing=None
    print(websocket.remote_address[0]+" connected")
    while True:
        if path[1:] == "send":
            msg =await websocket.recv()
            print(f"< {msg}")
            msg=json.loads(msg)
            if msg["type"] == "clipboard":
                pyperclip.copy(msg["data"])
            elif msg["type"]=="command":
                execute_commands(msg["data"])
            else:
                pass
            
            # await websocket.send(msg)
        elif path[1:] == "get":
            if not content==pyperclip.paste():
                content=pyperclip.paste()
                msg={"type":"clipboard","data":content}
                await send(websocket,msg)
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
                    await send(websocket,msg)
            elif theOS=="linux":
                pass
            elif theOS=="darwin":
                pass
            await asyncio.sleep(3)

        else:
            break

start_server = websockets.serve(mysocket, host=None,port=8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
logger = logging.getLogger('websockets.server')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())