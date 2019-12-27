import random
import socket
import urllib.request

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('151.217.111.34', 1234))


def get_offset():
    # load offset
    offset = urllib.request.urlopen('http://hoellipixelflut.de/xy/').read()

    x, y = offset.decode().split()
    return int(x), int(y)


def get_img():
    lines = urllib.request.urlopen(
        'http://hoellipixelflut.de/hoelli.csv').read()
    lines = lines.decode('utf-8').split('\n')[:-1]

    img = []
    for line in lines:
        img.append(line.replace(' ', '').split(','))

    h = len(img)
    w = len(img[0])

    return img, w, h


def pixel(x, y, r, g, b):
    cmd = ('PX %d %d %02x%02x%02x\n' % (x, y, r, g, b)).encode()
    sock.send(cmd)


dx, dy = get_offset()
print(dx, dy)

img, w, h = get_img()
print(w, h)

print('Start...')
while True:
    x = random.randint(0, w - 1)
    y = random.randint(0, h - 1)
    pixel(x + dx, y + dy, 255, 255, 0)
