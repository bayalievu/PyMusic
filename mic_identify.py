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


#list of identified songs
identified = []

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
	if len(identified) == 0 or identified[-1] != track_id:
		identified.append(track_id)
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
	conn = MySQLdb.connect(host= "localhost",user="root", passwd="123", db="pymusic",charset='utf8')

	import alsaaudio, wave, numpy

	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
	inp.setchannels(2)
	inp.setrate(44100)
	inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	inp.setperiodsize(1024)

	j=0
	while True:
		filename = 'test'+str(j)+'.wav'	
		w = wave.open(filename, 'w')
		w.setnchannels(2)
		w.setsampwidth(2)
		w.setframerate(44100)
		#Record 30 seconds and recognize
    		for i in range(int(30*44.1)):
			l, data = inp.read()
    			a = numpy.fromstring(data, dtype='int16')
    			w.writeframes(data)
		process_file(filename,conn)	
		os.remove(filename)
		j = j+1


	conn.close()	


