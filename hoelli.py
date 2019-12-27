import socket
import random
import time
import urllib.request

N_SOCKS = 16
L_CMD = 1024
DT = 60.0


def set_offset(sockets):
    # load offset
    offset = urllib.request.urlopen('http://hoellipixelflut.de/xy/').read()

    # send offset
    cmd = (f'OFFSET ').encode() + offset
    print(cmd)
    for sock in sockets:
        sock.send(cmd)


def main():
    # request and set offset
    lines = urllib.request.urlopen(
        'http://hoellipixelflut.de/hoelli.csv').read()
    lines = lines.decode('utf-8').split('\n')[:-1]

    img = []
    for line in lines:
        img.append(line.replace(' ', '').split(','))

    h = len(img)
    w = len(img[0])

    # connect
    sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM)
               for _ in range(N_SOCKS)]
    for sock in sockets:
        sock.connect(('151.217.111.34', 1234))

    set_offset(sockets)

    cmd = b''
    time0 = time.time()
    i = 0
    print("Let's Hölli...")
    while True:
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)

        rgb = img[y][x]
        if rgb == '000000':
            continue
        rgb = '00ff00'
        cmd += f'PX {x} {y} {rgb}'.encode()

        if True:
            sockets[i].send(cmd)
            cmd = b''
            i = (i + 1) % N_SOCKS

            if time.time() - time0 > DT:
                set_offset(sockets)
                time0 = time.time()


if __name__ == '__main__':
    main()
