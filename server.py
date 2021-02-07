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

# process = Popen(['python3', 'flaskserver.py'], stdout=PIPE, stderr=PIPE)

async def mysocket(websocket, path):
    content=""
    sent=""
    oldmsg=""
    playing=None
    # check os 
    theOS=platform.system().lower()
    print(websocket.remote_address)
    print("started")
    while True:
        if path[1:] == "send":
            if sent =="":
                msg =await websocket.recv()
                oldmsg=msg
                print(f"< {msg}")
            msg=json.loads(oldmsg)
            if msg["type"] == "clipboard":
                pyperclip.copy(msg["data"])
            elif msg["type"]=="command":
                if msg["data"]=="playPause":
                    pyautogui.press("playpause")
                if msg["data"]=="volumeUp":
                    pyautogui.press("volumeup")
                if msg["data"]=="volumeDown":
                    pyautogui.press("volumedown")
                if msg["data"]=="volumeMute":
                    pyautogui.press("volumemute")
                else:
                    
                    pass
            else:
                pass
            
            # await websocket.send(msg)
        elif path[1:] == "get":
            if not content==pyperclip.paste():
                content=pyperclip.paste()
                msg={"type":"clipboard","data":content}
                msg = json.dumps(msg)
                print(f"> {msg}")

                await websocket.send(msg)
            
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
                    msg=json.dumps(msg)
                    print(f"> {msg}")
                    await websocket.send(msg)
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