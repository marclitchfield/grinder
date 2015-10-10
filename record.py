import time
import sys

f = open('/dev/input/event0', 'rb')
t = time.time()

BUTTON = 0x04
DPAD = 0x03
START_BUTTON = 0x27

while True:
    timestamp = f.read(8)
    data = f.read(8)
    rest = ''
    kind = ord(data[0])

    if kind == DPAD:
        rest = f.read(16)
    elif kind == BUTTON:
        rest = f.read(32)
        button = rest[10]

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
