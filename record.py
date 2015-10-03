import time
import sys

f = open('/dev/input/event0', 'rb')
t = time.time()

BUTTON = 4
DPAD = 3
START_BUTTON = 27

while True:
    timestamp = f.read(8)
    data = f.read(8)
    rest = ''
    kind = ord(data[0])

    if kind == DPAD:
        rest = f.read(16)
    elif kind == BUTTON:
        rest = f.read(32)
        button = int(rest[10].encode('hex'))

        if button == START_BUTTON:
            sys.stderr.write('recording stopped\n')
            exit(0)
    else:
        print 'OR DIE', t
        exit(1)

    delay = str(time.time() - t)
    command = timestamp.encode('hex') + data.encode('hex') + rest.encode('hex')

    print delay + ',' + command

    t = time.time()
