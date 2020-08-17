import datetime as dt
import time

c = dt.datetime.now()

time.sleep(5)

t = dt.datetime.now()

diff = t-c
print(diff)