import urllib2
from datetime import datetime
from datetime import timedelta

# Name of the file stream and how long to record a sample
URL = "http://77.241.20.210:55655/stream1.mp3"
RECORD_SECONDS = 30

# Open the file stream and write file
filename = 'stream.mp3'
f=file(filename, 'wb')
url=urllib2.urlopen(URL)

# Basically a timer
t_start = datetime.now()
t_end = datetime.now()
t_end_old = t_end

# Record in chunks until
print "Recording..."
while t_end-t_start < timedelta(seconds=RECORD_SECONDS):
    f.write(url.read(1024))
    t_end = datetime.now()
