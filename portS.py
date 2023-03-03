import socket
import argparse
import os
import pyfiglet
import keyboard as kb
import uuid
from datetime import datetime
from time import sleep


parse = argparse.ArgumentParser()

parse.add_argument('-hs', '--host')
parse.add_argument('-p', '--port', required=False, action='store_true')

args = parse.parse_args()

HOST = str(args.host)


def portScan(host):
    filename = str(uuid.uuid4())
    maxRange = 1025
    
    try:
        if args.port:
            maxRange = 65535

        banner()
        closePorts = 0
        for port in range(1, maxRange):

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(2)

            connect = sock.connect_ex((host, port))

            service = getService(host, port)
            version = getServiceVersion(host, port)

            if type(version) == None:
                version = '-'

            if connect == 0:
                with open(filename, 'a') as output:
                    output.writelines(
                        f'{port}/tcp   open        {service}      {version}\n')
            else:
                closePorts += 1
                pass

        print(f'Host shown {closePorts} closed ports')
        print('PORT     STATUS      SERVICE     VERSION')
        
        with open(filename, 'r') as o:
            print(o.read())
            
        if os.path.exists(filename):
            os.remove(filename)
            
    except KeyboardInterrupt:
        print('App Aborted')
        
        if os.path.exists(filename):
            os.remove(filename)
            
        exit(1)


def getService(host, port):
    try:
        service = socket.getservbyport(port, 'tcp')
        
        return service
    except:
        pass


def getServiceVersion(host, port):
    try:
        payloadHTTP = b'GET / HTTP/1.0\r\n\r\n"'

        sock = socket.socket()

        if port == 80:
            sock.connect((host, payloadHTTP))
            
            return sock.recv(1024)
        else:
            sock.connect((host, port))
            sock.send(b'A')
            
            return sock.recv(1024)
    except:
        pass


def banner():
    now = datetime.now()
    banner = pyfiglet.Figlet(font='slant')
    print(banner.renderText('PortMap'))
    print(f'Starting Scan ( https://github.com/JPedroVentura ) at {now}')
    print('Host is Up')
    print(f'Port Scan Report for {HOST}')


portScan(HOST)
