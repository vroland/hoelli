import random
import socket
import time
import urllib.request
import sys

DT_OFFSET = 20.0
DT_IMG = 60.0
MAX_SOCKS = 32


def get_offset(px_cnt=0):
    print('Retrieving offset...', end='', flush=True)

    # load offset
    url = 'http://hoellipixelflut.de/xy/?report={px_cnt}'.format(px_cnt=px_cnt)
    offset = urllib.request.urlopen(url).read()

    x, y = offset.decode().split()

    x = int(x)
    y = int(y)

    print(' Done. New offset:', x, y)

    return x, y


def get_cmds():
    print('Retrieving image...', end='', flush=True)

    lines = urllib.request.urlopen(
        'http://hoellipixelflut.de/hoelli.csv').read()
    lines = lines.decode('utf-8').split('\n')[:-1]

    img = []
    for line in lines:
        img.append(line.replace(' ', '').split(','))

    h = len(img)
    w = len(img[0])

    cmds = []
    for y in range(h):
        for x in range(w):
            rgb = img[y][x]
            if rgb == '000000':
                continue
            int(rgb, 16)
            if len(rgb) != 6:
                raise ValueError()
            cmds.append('PX {xx} {yy} {rgb}\n'.format(
                xx=x, yy=y, rgb=rgb).encode())

    print(' Done. New image dimensions:', w, h)

    random.shuffle(cmds)

    return cmds


def main():
    # connect
    print('Connecting to the C3 Pixel Flut wall...', end='', flush=True)
    sockets = []
    for _ in range(MAX_SOCKS):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(('151.217.111.34', 1234))
        except ConnectionRefusedError:
            break
        sockets.append(sock)

    if len(sockets) < 1:
        raise ConnectionRefusedError('Could not connect with any socket.')

    print(' Connected with {} sockets.'.format(len(sockets)))

    dx, dy = get_offset()

    cmds = get_cmds()

    print('Let\'s Hölli...')

    time0 = time.time()
    time1 = time.time()
    i_sock = 0
    px_cnt = 0
    i = 0
    while True:
        for cmd in cmds:
            sockets[i_sock].send(cmd)
            px_cnt += 1
            i_sock = (i_sock + 1) % len(sockets)

            if i % 4096 == 0:
                if time.time() - time0 > DT_OFFSET:
                    dx, dy = get_offset(px_cnt)
                    time0 = time.time()
                    px_cnt = 0

                if time.time() - time1 > DT_IMG:
                    pixels, w, h = get_cmds()
                    time1 = time.time()
            i += 1


if __name__ == '__main__':
    print('USAGE: python3 hoelli.py [MAX_SOCKETS]')
    if len(sys.argv) > 1:
        MAX_SOCKS = int(sys.argv[1])
    while True:
        try:
            main()
        except Exception as e:
            print('An exception encountered: ', type(e),  e)
