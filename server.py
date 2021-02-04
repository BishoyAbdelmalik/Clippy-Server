# WS server example

import asyncio
import websockets
import logging
import pyperclip
import json
import pyautogui
async def mysocket(websocket, path):
    content=""
    print("started")
    while True:
        if path[1:] == "send":
            msg =await websocket.recv()
            msg=json.loads(msg)
            print(f"< {msg}")
            if msg["type"] == "clipboard":
                pyperclip.copy(msg["data"])
            elif msg["type"]=="command":
                if msg["data"]=="playPause":
                    pyautogui.press("playpause")
                if msg["data"]=="volumeUp":
                    pyautogui.press("volumeup")
                if msg["data"]=="volumeDown":
                    pyautogui.press("volumedown")
            else:
                pass
            
            # await websocket.send(msg)
        elif path[1:] == "getClipboard":
            if not content==pyperclip.paste():
                content=pyperclip.paste()
                msg={"type":"clipboard","data":content}
                msg = json.dumps(msg)
                print(f"> {msg}")

                await websocket.send(msg)
            await asyncio.sleep(3)

        else:
            break

start_server = websockets.serve(mysocket, host=None,port=8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
logger = logging.getLogger('websockets.server')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())