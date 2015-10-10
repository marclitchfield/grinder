import os
import sys
import subprocess
import time
import signal
import threading
from fcntl import fcntl, F_GETFL, F_SETFL

recordscript = 'record.sh'
inputdevice = '/dev/input/event0'
configfolder = './config'
recordfile = os.path.join(configfolder, 'record')
playfile = os.path.join(configfolder, 'play')
stopfile = os.path.join(configfolder, 'stop')

state = 'ready'
currentprocess = None

def record():
    print "RECORDING"

def play():
    print "PLAYING"

def stop():
    print "STOPPED"

positions = {}

def resetpositions():
    global positions
    positions = dict(map(lambda a: (a, 0), actions.keys()))

actions = dict(record=record, play=play, stop=stop)
resetpositions()
sequences = {}

def configured():
    if not os.path.exists(configfolder):
        return False 
    if not os.path.exists(recordfile):
        return False 
    if not os.path.exists(playfile):
        return False 
    if not os.path.exists(stopfile):
        return False
    return True

class DeviceRecorder:
    def __init__(self):
        self.recording = False
        
    def record(self, filename):
        dev = open(inputdevice, 'rb')
        out = open(filename, 'wb')
        flags = fcntl(dev.fileno(), F_GETFL) 
        fcntl(dev.fileno(), F_SETFL, flags | os.O_NONBLOCK)
        self.recording = True
        while self.recording:
            try:
                out.write(os.read(dev.fileno(), 16)) 
            except OSError:
                time.sleep(0.2)
        out.close()
        dev.close()

    def stop(self):
        self.recording = False

def configure():
    if not os.path.exists(configfolder):
        os.mkdir(configfolder)
    recordaction('RECORD', recordfile)
    recordaction('PLAY', playfile)
    recordaction('STOP', stopfile)

def recordaction(action, filename):
    print "Press key sequence for %s, then press <enter>" % action
    recorder = DeviceRecorder()
    thread = threading.Thread(target=recorder.record, args=[filename])
    thread.start()
    sys.stdin.readline();
    recorder.stop()
    thread.join()

def actionfile(action):
    return os.path.join(configfolder, action)

def loadsequences():
    for action in actions.keys():
        sequences[action] = loadsequence(actionfile(action))

def loadsequence(sequencefile):
    f = open(sequencefile, 'rb')
    data = f.read()
    commands = []
    for i in xrange(0, len(data), 16):
        commands.append(data[i+8:i+16])
    return commands

def findaction(command):
    for action, commands in sequences.iteritems():
        if commands[positions[action]] == command:
            positions[action] += 1
            if len(commands) == positions[action]:
                resetpositions()
                return actions[action]
        else:
            positions[action] = 0
    return None

def listen():
    eventstream = open(inputdevice, 'rb')
    print 'Listening for commands...'

    while True:
        line = eventstream.read(16)
        command = line[8:16]
        actionfunction = findaction(command)
        if actionfunction != None:
            currentprocess = actionfunction()

if not configured():
    configure()

loadsequences()
listen()
