import socket
import urllib.request

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('151.217.111.34', 1234))


def get_offset():
    # load offset
    offset = urllib.request.urlopen('http://hoellipixelflut.de/xy/').read()

    x, y = offset.decode().split()
    return int(x), int(y)


def pixel(x, y, r, g, b):
    cmd = ('PX %d %d %02x%02x%02x\n' % (x, y, r, g, b)).encode()
    sock.send(cmd)


dx, dy = get_offset()
print(dx, dy)

w = 20
h = 20

print('Start...')
while True:
    for x in range(w):
        for y in range(h):
            pixel(x + dx, y + dy, 0, 255, 0)
