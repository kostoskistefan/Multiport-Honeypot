import sys
import time
from socket import * 
import argparse
import select

LOG_PATH = '.'
HOST = ''

sockets = []

def writeLog(client, protocol):
    fopen = open(LOG_PATH + '/honey.txt', 'a')
    fopen.write('Time: %s\nIP: %s\nPort: %d\nProtocol: %s\n\n' % (time.ctime(), client[0], client[1], protocol))
    fopen.close()

def createSocket(port, protocol):
    s = socket(AF_INET, protocol)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((HOST, port))
    return s

def createTCPSocket(port):
    s = createSocket(port, SOCK_STREAM)
    s.listen(1)
    return s

def createUDPSocket(port):
    return createSocket(port, SOCK_DGRAM)

def main(ports):
    for port in ports:
        sockets.append(createTCPSocket(port))
        sockets.append(createUDPSocket(port))

    while True:
        readable,_,_ = select.select(sockets, [], [])
        ready = readable[0]

        address = ''
        protocol = ''

        if ready.type == SocketKind.SOCK_DGRAM:
            _, address = ready.recvfrom(1024)
            protocol = 'UDP'

        elif ready.type == SocketKind.SOCK_STREAM:
            sock, address = ready.accept()
            sock.close()
            protocol = 'TCP'

        writeLog(address, protocol)

if __name__=='__main__':
    try:
        parser = argparse.ArgumentParser(prog='python3 honeypot.py', formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='Multi-Port Honeypot')
        req_grp = parser.add_argument_group(title='required arguments')
        req_grp.add_argument('-p', '--ports', help="Comma separated port numbers (ex. 21,22,23)")
        req_grp.add_argument('-a', '--host', help="IP address of your network interface (ex. 192.168.0.105)")
        parser.add_argument('-o', '--output', help="Path to the directory where the log will be saved")
        args = parser.parse_args()

        if not args.ports or not args.host:
            parser.print_help()
            sys.exit()

        if args.output:
            LOG_PATH = args.output

        if args.host:
            HOST = args.host

        port, *remaining = args.ports.split(',')
        ports = list(map(int, [port] + remaining))

        main(ports)
    except (KeyboardInterrupt, SystemExit):
        exit(0)
    except BaseException as e:
        print('Error: ' + str(e))
        exit(1)
