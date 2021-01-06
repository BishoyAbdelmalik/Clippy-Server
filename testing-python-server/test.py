# WS server example

import asyncio
import websockets
import logging
import pyperclip

async def hello(websocket, path):
    content=""
    while True:
        print(path[1:])
        if int(path[1:]) == 1:
            msg = await websocket.recv()
            print(f"< {msg}")
            pyperclip.copy(msg)
            await websocket.send(msg)
        elif int(path[1:]) == 0:
            if not content==pyperclip.paste():
                content=pyperclip.paste()
                await websocket.send(content)
            await asyncio.sleep(3)

        else:
            break

start_server = websockets.serve(hello, host=None,port=8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
logger = logging.getLogger('websockets.server')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())