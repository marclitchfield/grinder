import sys
import time
import csv

f = open('/dev/input/event0', 'wb')
times = int(sys.argv[2])

for i in range(times):
    inp = csv.reader(open(sys.argv[1]))
    for command in inp:
        time.sleep(float(command[0]))
        print(command[1])
        f.write(command[1].decode('hex'))
        f.flush()
