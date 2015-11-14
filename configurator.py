import os
import sys
from recorder import Recorder

class Configurator:

    def __init__(self, configfolder, inputdevice):
        self._configfolder = configfolder
        self._inputdevice = inputdevice
        self._recordfile = os.path.join(configfolder, 'record')
        self._playfile = os.path.join(configfolder, 'play')
        self._stopfile = os.path.join(configfolder, 'stop')

    def configure(self):
        if not self._configured():
            if not os.path.exists(self._configfolder):
                os.mkdir(self._configfolder)
            self._recordaction('RECORD', self._recordfile)
            self._recordaction('PLAY', self._playfile)
            self._recordaction('STOP', self._stopfile)

    def _configured(self):
        if not os.path.exists(self._configfolder):
            return False 
        if not os.path.exists(self._recordfile):
            return False 
        if not os.path.exists(self._playfile):
            return False 
        if not os.path.exists(self._stopfile):
            return False
        return True

    def _recordaction(self, action, filename):
        print "Press key sequence for %s, then press <enter>" % action
        recorder = Recorder()
        recorder.start(filename, self._inputdevice)
        sys.stdin.readline();
        recorder.stop()
