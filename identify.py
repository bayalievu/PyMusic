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
    	else:
        	print "Couldn't decode", file
		return

	if track_id is None:
		print "No match found for the file"
		return
	else:
		print track_id
	
	#Insert tracks only once
	if len(identified) == 0 or identified[-1] != track_id:
		identified.append(track_id)
		now = time.strftime('%Y-%m-%d %H:%M:%S')
	
		db = conn.cursor()

		try:
	   		print "Inserting track_id: " + track_id	+ " for file: " + filename
	   		db.execute("""INSERT INTO played_melody(track_id,melody_id,radio,time_played) VALUES (%s,%s,%s,%s)""",(track_id,None,"EuropaPlus",now))
	   		conn.commit()
		except db.Error, e:
           		print "Error %d: %s" % (e.args[0],e.args[1])
	   		conn.rollback()
	else:
		print "Track is already recognized from other file"

if __name__ == "__main__":
	conn = MySQLdb.connect(host= "localhost",user="root", passwd="123", db="pymusic",charset='utf8')

	
	segment = AudioSegment.from_mp3("/home/ulan/Music/Europa1.mp3")

	# pydub does things in miliseconds
	ten_minutes = 0.5 * 60 * 1000
	one_minute = 1 * 60 * 1000
	half_minute = 30 * 1000

	length = len(segment)

	ten_parts = length/ten_minutes

	for i in range(ten_parts):
		part = segment[i*ten_minutes:(i+1)*ten_minutes]
		part.export("/home/ulan/PyMusic/mp3/"+str(i)+".mp3", format="mp3",bitrate="128k")
    	

	# Process files sorted by modified time
	files = sorted(glob('/home/ulan/PyMusic/mp3/*.mp3'), key=os.path.getmtime) 
	files.sort()
	print "Number of files: "+ str(len(files))
	for filename in files:
       		process_file(filename,conn)
	
	conn.close()	
