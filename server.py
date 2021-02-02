# WS server example

import asyncio
import websockets
import logging
import pyperclip
import json
async def mysocket(websocket, path):
    content=""
    
    print("started")
    while True:
        print(path[1:])
        if path[1:] == "1":
            msg = await websocket.recv()
            msg=json.loads(msg)
            print(f"< {msg}")
            if msg["type"] == "clipboard":
                pyperclip.copy(msg["data"])
            else:
                pass
            # await websocket.send(msg)
        elif path[1:] == "getClipboard":
            if not content==pyperclip.paste():
                content=pyperclip.paste()
                msg={"type":"clipboard","data":content}
                msg = json.dumps(msg)
                print(msg)
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