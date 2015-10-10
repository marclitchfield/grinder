import time
import struct
import sys

def readshort(data, offset):
    return struct.unpack('<H', data[offset:offset+2])[0]

def readlong(data, offset):
    return struct.unpack('<L', data[offset:offset+4])[0]

def readtimestamp(data, offset):
    timeoffset = (readlong(data, offset), readlong(data, offset+4))
    return timeoffset[0] + timeoffset[1]/1000000.0

def events(data):
    lastseconds = None
    lasteventtime = None
    commands = []
    for i in xrange(0, len(data), 16):
        seconds = readtimestamp(data, i)
        command = data[i:i+16]
        if lastseconds and lastseconds != seconds:
            timedelta = lastseconds - lasteventtime if lasteventtime else 0
            lasteventtime = lastseconds
            yield (timedelta, commands)
            commands = []
        lastseconds = seconds
        commands.append(command)
    if lastseconds:
        timedelta = lastseconds - lasteventtime if lasteventtime else 0
        yield (timedelta, commands)

def replay(eventsequence):
    out = open('/dev/input/event0', 'wb')
    eventlist = list(eventsequence)
    while True:
        for event in eventlist:
            (timedelta, commands) = event
            time.sleep(timedelta)
            data = reduce(lambda data, command: data + command, commands, '')
            out.write(data)
            out.flush()
        time.sleep(2)

filename = sys.argv[1]
replay(events(open(filename, 'rb').read()))
