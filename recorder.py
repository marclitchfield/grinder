import threading
import signal
import os
import time
from fcntl import fcntl, F_GETFL, F_SETFL

class Recorder:

    def start(self, filename, device):
        self._thread = threading.Thread(target=self._record, args=[filename, device])
        self._thread.start()
        
    def stop(self):
        self._recording = False
        self._thread.join()

    def _record(self, filename, device):
        dev = open(device, 'rb')
        out = open(filename, 'wb')
        flags = fcntl(dev.fileno(), F_GETFL) 
        fcntl(dev.fileno(), F_SETFL, flags | os.O_NONBLOCK)
        self._recording = True
        while self._recording:
            try:
                out.write(os.read(dev.fileno(), 16)) 
            except OSError:
                time.sleep(0.2)
        out.close()
        dev.close()
