import socket
import urllib.request

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('151.217.111.34', 1234))


def set_offset(socket):
    # load offset
    offset = urllib.request.urlopen('http://hoellipixelflut.de/xy/').read()

    # send offset
    cmd = (f'OFFSET ').encode() + offset
    print(cmd)
    socket.send(cmd)


def pixel(x, y, r, g, b):
    cmd = ('PX %d %d %02x%02x%02x\n' % (x, y, r, g, b)).encode()
    sock.send(cmd)


set_offset(sock)

w = 20
h = 20

print('Start...')
while True:
    for x in range(w):
        for y in range(h):
            pixel(x, y, 0, 255, 0)
