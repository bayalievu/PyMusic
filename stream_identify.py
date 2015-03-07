from pydub import AudioSegment
import sys
sys.path.insert(0, "/home/ulan/echoprint-server/API")
import MySQLdb
import os
import subprocess
import time    
from glob import glob
import fp

codegen_path = os.path.abspath("/home/ulan/echoprint-codegen/echoprint-codegen")

try:
    import json
except ImportError:
    import simplejson as json


#last identified song
last_track = None

def codegen(file, start=0, duration=30):
    	proclist = [codegen_path, os.path.abspath(file), "%d" % start, "%d" % duration]
    	p = subprocess.Popen(proclist, stdout=subprocess.PIPE)                      
    	code = p.communicate()[0]                                                   
    	return json.loads(code)

def process_file(filename,conn):
	print filename,
    	codes = codegen(filename)
	track_id = None
    	if len(codes) and "code" in codes[0]:
        	decoded = fp.decode_code_string(codes[0]["code"])
        	result = fp.best_match_for_query(decoded)
        	if result.TRID:
			track_id = result.TRID
			print track_id
		else:
			print "No match found for the file"
			return
		
    	else:
        	print "Couldn't decode", file
		return

	#Insert tracks only once
	if last_track is None or last_track != track_id:
		last_track =  track_id
		now = time.strftime('%Y-%m-%d %H:%M:%S')
	
		db = conn.cursor()

		try:
	   		print "Inserting track_id: " + track_id	+ " for file: " + filename
	   		db.execute("""INSERT INTO played_melody(track_id,melody_id,radio,time_played) VALUES (%s,%s,%s,%s)""",(track_id,None,"Min-Kiyal",now))
	   		conn.commit()
		except db.Error, e:
           		print "Error %d: %s" % (e.args[0],e.args[1])
	   		conn.rollback()
	else:
		print "Track is already recognized from other file"

if __name__ == "__main__":
	
        if len(sys.argv) < 3:
                print "Usage: python stream_identify.py radio stream"
                exit()

        radio = sys.argv[1]
        stream = sys.argv[2]

	conn = MySQLdb.connect(host= "localhost",user="root", passwd="123", db="pymusic",charset='utf8')
	import urllib2
	from datetime import datetime
	from datetime import timedelta

	while True:
		now = time.strftime('%Y-%m-%d %H:%M:%S')
		filename = radio+now+'.mp3'
		f=file(filename, 'wb')
		url=urllib2.urlopen(stream)

		# Basically a timer
		t_start = datetime.now()
		t_end = datetime.now()
		t_end_old = t_end

		# Record in chunks until
		while t_end-t_start < timedelta(seconds=30):
    			f.write(url.read(1024))
    			t_end = datetime.now()
		
		process_file(filename,conn)	


	conn.close()	


