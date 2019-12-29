import random
import socket
import time
import urllib.request
import sys
import selectors
import threading

sel = selectors.DefaultSelector()

DT = 10.0
MAX_SOCKS = 10


def call_api(px_cnt=0):
    # load offset
    url = 'http://hoellipixelflut.de/client-api/?report={px_cnt}'.format(
        px_cnt=px_cnt)
    response = urllib.request.urlopen(url).read()

    x, y, url = response.decode().split()

    x = int(x)
    y = int(y)
    url = 'http://hoellipixelflut.de/images/' + url

    return x, y, url


def load_img(url):
    print('Retrieving image...', end='', flush=True)

    lines = urllib.request.urlopen(url).read()
    lines = lines.decode('utf-8').split('\n')[:-1]

    img = []
    for line in lines:
        img.append(line.replace(' ', '').split(','))

    print(' Done. New image dimensions:', len(img[0]), len(img))

    return img


def get_cmds(dx, dy, img):
    print('Updating command list...', end='', flush=True)
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
                xx=x+dx, yy=y+dy, rgb=rgb).encode())

    random.shuffle(cmds)
    print(' Done.')

    return cmds

current_commands = b''
interval_pixel_count = 0

pixels_per_batch = 0

sockbuf = {}
def send(sock):
    global interval_pixel_count

    try:
        data = sockbuf.get(sock, b'')
        sent = sock.send(data)
        sockbuf[sock] = data[sent:]
        if len(data) == 0:
            sockbuf[sock] = current_commands

    except Exception as e:
        print('An exception encountered: ',
              type(e),  e, ' . Restarting...')
        sel.unregister(sock)
        sock.close()
        connect_socket()
        return

    interval_pixel_count += pixels_per_batch

def update_commands():
    global current_commands
    global interval_pixel_count
    global pixels_per_batch

    print ("updating image...")
    dx, dy, url = call_api(interval_pixel_count)
    img = load_img(url)
    cmds = get_cmds(dx, dy, img)
    current_commands = b''.join(cmds)
    pixels_per_batch = len(cmds)
    for k in sockbuf:
        sockbuf[k] = current_commands

def update_loop():
    global interval_pixel_count

    while True:
        t1 = time.time()
        update_commands()
        print ("updating took", time.time() - t1, "seconds")
        interval_pixel_count = 0
        time.sleep(10)

def connect_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #sock.connect(('wall2.c3pixelflut.de', 1234))
        #sock.connect(('ftp.agdsn.de', 443))

        sock.connect(('151.217.118.128', 1234))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**18)
        sel.register(sock, selectors.EVENT_WRITE, send)
        sock.setblocking(0)
        print ("connected!")
    except ConnectionRefusedError:
        return None
    return sock

def main():
    global interval_pixel_count

    # connect
    print('Connecting to the C3 Pixel Flut wall...', end='', flush=True)
    for _ in range(MAX_SOCKS):
        connect_socket()

    if len(sel.get_map()) < 1:
        raise ConnectionRefusedError('Could not connect with any socket.')

    print(' Connected with {} sockets.'.format(len(sel.get_map())))

    update_commands()

    print('Let\'s Hölli...')


    while True:
        events = sel.select()
        for key, mask in events:
            send(key.fileobj)

if __name__ == '__main__':
    print('USAGE: python3 hoelli.py [MAX_SOCKETS]')
    if len(sys.argv) > 1:
        MAX_SOCKS = int(sys.argv[1])

    update_thread = threading.Thread(target=update_loop)
    update_thread.start()

    main()
