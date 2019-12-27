import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('151.217.111.34', 1234))


def pixel(x, y, r, g, b):
    cmd = ('PX %d %d %02x%02x%02x\n' % (x, y, r, g, b)).encode()
    print(cmd)
    sock.send(cmd)


w = 20
h = 20

while True:
    for x in range(w):
        for y in range(h):
            pixel(x, y, 0, 255, 0)
