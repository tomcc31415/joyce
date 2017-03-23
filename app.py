#!/bin/python

import socket
import time

import logging


def accept(port):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', port))
    sock.listen(1)
    return sock.accept()

def main(port, files):
    logging.debug('main called with port={}, files={}'.format(port, files))

    lines = []
    for file in files:
        with open(file) as input:
            lines += input.readlines()

    while True:
        logging.info('waiting for connection on port {}'.format(port))
        conn, addr = accept(port)
        logging.info('connection from: {}'.format(addr))
        try:
            while True:
                for line in lines:
                    conn.sendall(line)
                    time.sleep(0.03)
        except socket.error as e:
            logging.debug('received socket error: {}'.format(e))
        finally:
            logging.debug('closing connection')
            conn.close()
        

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    main(8080, ['vvd2017.txt', 'cda2017.txt', 'gl2017.txt'])
