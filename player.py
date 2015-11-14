import eventstream
import time
import threading

class Player:

    def start(self, filename, device):
        self._thread = threading.Thread(target=self._replay, args=[filename, device])
        self._thread.start()

    def stop(self):
        self._playing = False
        self._thread.join()

    def _replay(self, filename, device):
        self._playing = True
        out = open(device, 'wb')
        eventlist = list(self._events(open(filename, 'rb').read()))
        while self._playing:
            for event in eventlist:
                (timedelta, commands) = event
                time.sleep(timedelta)
                data = reduce(lambda data, command: data + command, commands, '')
                out.write(data)
                out.flush()
            time.sleep(.5)

    def _events(self, data):
        lastseconds = None
        lasteventtime = None
        commands = []
        
        for i in xrange(0, len(data), 16):
            seconds = eventstream.readtimestamp(data, i)
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

