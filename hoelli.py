import random
import socket
import time
import urllib.request


def get_offset(px_cnt=0):
    # load offset
    url = f'http://hoellipixelflut.de/xy/?report={px_cnt}'
    offset = urllib.request.urlopen(url).read()

    x, y = offset.decode().split()
    print('New offset: ', x, y)
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


def main():
    DT = 20.0
    N_SOCKS = 16

    # connect
    sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM)
               for _ in range(N_SOCKS)]
    for sock in sockets:
        sock.connect(('151.217.111.34', 1234))

    dx, dy = get_offset()
    print(dx, dy)

    img, w, h = get_img()
    print(w, h)

    print('Start...')
    time0 = 0
    i_sock = 0
    px_cnt = 0
    while True:
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)

        rgb = img[y][x]
        if rgb == '000000':
            continue

        cmd = f'PX {x + dx} {y + dy} {rgb}\n'.encode()
        sockets[i_sock].send(cmd)
        px_cnt += 1
        i_sock = (i_sock + 1) % N_SOCKS

        if time.time() - time0 > DT:
            dx, dy = get_offset(px_cnt)
            time0 = time.time()
            px_cnt = 0


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception:
            pass
