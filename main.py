from configurator import Configurator
from listener import Listener

inputdevice = '/dev/input/event0'
configfolder = './config'

Configurator(configfolder, inputdevice).configure()
listener = Listener(configfolder, inputdevice)

try:
    listener.listen()
except KeyboardInterrupt:
    listener.stop()
