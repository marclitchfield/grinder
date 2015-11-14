import struct

def readtimestamp(data, offset):
    timeoffset = (_readlong(data, offset), _readlong(data, offset+4))
    return timeoffset[0] + timeoffset[1]/1000000.0

def _readshort(data, offset):
    return struct.unpack('<h', data[offset:offset+2])[0]

def _readlong(data, offset):
    return struct.unpack('<l', data[offset:offset+4])[0]
