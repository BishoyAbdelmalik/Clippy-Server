import asyncio
import websockets
import sys
import json
async def send_to_client(websocket,msg:dict)->None:
    if not isinstance(msg,dict):
        raise TypeError("msg need to be a dict") 
    else:
        msg_str=json.dumps(msg)
        print(f"> {msg_str}")
        await websocket.send(msg_str)

# TODO change the url to dynamic change based on input from websocket file
async def send():
    uri = "ws://localhost:8765/send"
    if len(sys.argv)!=2:
        return
    async with websockets.connect(uri) as websocket:
        
        path=sys.argv[1]
        
        msg={"type": "info_send_file","data": path}
        print(f"> {sys.argv[1]}")
        await send_to_client(websocket,msg)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send())