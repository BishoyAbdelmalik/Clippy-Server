import socket
import os

def create_dir_if_missing(path:str):
    if not os.path.exists(path):
        os.makedirs(path)

def get_my_ip_address(remote_server="google.com"):
    """
    Return the/a network-facing IP number for this system.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s: 
        s.connect((remote_server, 80))
        return s.getsockname()[0]
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0
def get_flask_port_when_up(path:str) -> int:
    """
        waits for flask to be up then return port
    """
    import time
    while not os.path.exists(path):
        print("flask config missing")
        time.sleep(0.5)
        pass
    while True:
        import json
        import requests
        line='{"port":-1}'
        with open(path,"r") as f:
            line=f.readline()
        port=json.loads(line)["port"]
        if is_port_in_use(port):
            try:
                requests.get("http://localhost:"+str(port)+"/")
                return port 
            except:
                time.sleep(0.5)
        else:
            time.sleep(0.5)
        
        
    