import os

from player import Player
from recorder import Recorder

class Listener:

    def __init__(self, configfolder, inputdevice):
        self._configfolder = configfolder
        self._positions = {}
        self._sequences = {}
        self._actions = dict(record=self._record, play=self._play, stop=self._stop)
        self._datafile = os.path.join(configfolder, 'coolmoves')
        self._inputdevice = inputdevice
        self._vcr = None

    def stop(self):
        self._listening = False
        self._stop()

    def listen(self):
        self._resetpositions()
        self._loadsequences()
        eventstream = open(self._inputdevice, 'rb')
        self._listening = True
        print 'Listening for commands...'

        while self._listening:
            line = eventstream.read(16)
            command = line[8:16]
            actionfunction = self._findaction(command)
            if actionfunction != None:
                currentprocess = actionfunction()

    def _actionfile(self, action):
        return os.path.join(self._configfolder, action)

    def _loadsequences(self):
        for action in self._actions.keys():
            self._sequences[action] = self._loadsequence(self._actionfile(action))

    def _loadsequence(self, sequencefile):
        f = open(sequencefile, 'rb')
        data = f.read()
        commands = []
        for i in xrange(0, len(data), 16):
            commands.append(data[i+8:i+16])
        return commands

    def _findaction(self, command):
        for action, commands in self._sequences.iteritems():
            if commands[self._positions[action]] == command:
                self._positions[action] += 1
                if len(commands) == self._positions[action]:
                    self._resetpositions()
                    return self._actions[action]
            else:
                self._positions[action] = 0
        return None

    def _resetpositions(self):
        self._positions = dict(map(lambda a: (a, 0), self._actions.keys()))

    def _record(self):
        if not self._vcr:
            print "RECORDING"
            self._vcr = Recorder()
            self._vcr.start(self._datafile, self._inputdevice)

    def _play(self):
        if not self._vcr and os.path.exists(self._datafile):
            print "PLAYING"
            self._vcr = Player()
            self._vcr.start(self._datafile, self._inputdevice)

    def _stop(self):
        if self._vcr:
            print "STOPPED"
            self._vcr.stop()
            self._vcr = None

