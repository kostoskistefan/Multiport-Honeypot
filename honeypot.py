import sys
import time
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
        parser = argparse.ArgumentParser(prog='python3 honeypot.py', formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='Multi-Port Honeypot')
        req_grp = parser.add_argument_group(title='required arguments')
        req_grp.add_argument('-p', '--ports', nargs='+', help="Comma separated port numbers (ex. 21,22,23)")
        req_grp.add_argument('-a', '--host', nargs='+', help="IP address of your network interface (ex. 192.168.0.105)")
        parser.add_argument('-o', '--output', nargs='?', default='./', help="Path to the directory where the log will be saved")
        args = parser.parse_args()

        if not args.ports or not args.host:
            parser.print_help()
            sys.exit()

        if args.output:
            LOG_PATH = [args.output[:-1] if args.output[-1] == '/' else args.output];

        if args.host:
            HOST = args.host;

        main(args.ports.split(","))
    except (KeyboardInterrupt, SystemExit):
        exit(0)
    except BaseException as e:
        print('Error: ' + str(e))
        exit(1)
