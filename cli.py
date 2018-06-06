import sys
import time

for i in range(100):
    time.sleep(1)
    # sys.stdout.write("\r%d%%" % i)
    # sys.stdout.flush()
    print("\r{0}%".format(i), end=str())