import socket
import sys, select
from threading import Thread
import time
import json
import os

# first check for config.json
config_file_check = os.path.isfile('config.json')
if config_file_check is True:
    config = json.load(open('config.json', 'r'))
elif config_file_check is False:
    print('no config found, creating new , to change settings edit config.json')
    config = {}
    config['serverIp'] = input('server ip ?')
    config['serverPort'] = int(input('server port?'))
    config['adminPasswd'] = input('admin password?')
    with open('config.json', 'w') as file:
        json.dump(config, file)
        file.close()

# variables
running = True
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((config['serverIp'], config['serverPort']))
def listen():
    while True:
        try:
            sock.settimeout(0.5)
            print(sock.recv(512).decode(), end='\r\n')
        except socket.timeout:
            pass


Thread(target=listen).start()
while True:
    time.sleep(0.5)
    try:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = input()
            sock.send(bytes('{}\r\n'.format(line), 'utf-8'))
            continue
    except socket.timeout:
        pass
