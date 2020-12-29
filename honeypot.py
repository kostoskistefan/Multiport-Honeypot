import time
import threading
import socket
import argparse
import select

LOG_PATH = '.'
HOST = ''

sockets = []

def writeLog(client):
    separator = '=' * 50
    fopen = open(LOG_PATH + '/honey.log', 'a')
    fopen.write('Time: %s\nIP: %s\nPort: %d\n%s\n\n'%(time.ctime(), client[0], client[1], separator))
    fopen.close()

def main(ports):
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, int(port)))
        s.listen(1)

        sockets.append(s)

    while True:
        readable,_,_ = select.select(sockets, [], [])
        ready = readable[0]
        sock, address = ready.accept()
        sock.close()
        writeLog(address)

if __name__=='__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--ports')
        parser.add_argument('-a', '--host')
        parser.add_argument('-o', '--output')
        args = parser.parse_args()

        if args.output:
            LOG_PATH = args.output;

        if args.host:
            HOST = args.host;

        main(args.ports.split(","))
    except (KeyboardInterrupt, SystemExit):
        exit(0)
    except BaseException as e:
        print('Error: ' + str(e))
        exit(1)
