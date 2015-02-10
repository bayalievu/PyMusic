from pydub import AudioSegment
import sys
sys.path.insert(0, "/home/ulan/echoprint-server/API")
import MySQLdb
import os
import subprocess
import time    
from glob import glob
import fp

try:
    import json
except ImportError:
    import simplejson as json

codegen_path = os.path.abspath("/home/ulan/echoprint-codegen/echoprint-codegen")

def codegen(file, start=0, duration=30):
    	proclist = [codegen_path, os.path.abspath(file), "%d" % start, "%d" % duration]
    	p = subprocess.Popen(proclist, stdout=subprocess.PIPE)                      
    	code = p.communicate()[0]                                                   
    	return json.loads(code)

def process_file(filename,conn):
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
		print "No match found for the file: " +filename
		return
	
	now = time.strftime('%Y-%m-%d %H:%M:%S')
	
	db = conn.cursor()

	try:
	   db.execute("""INSERT INTO played_melody(track_id,melody_id,radio,time_played) VALUES (%s,%s,%s,%s)""",(track_id,None,"EuropaPlus",now))
	   print "INSERT INTO played_melody(track_id,melody_id,radio,time_played) VALUES (%s,%s,%s,%s) " + track_id	
	   conn.commit()
	except:
	   conn.rollback()


if __name__ == "__main__":
	conn = MySQLdb.connect(host= "localhost",user="root", passwd="123", db="pymusic",charset='utf8')

	'''
	segment = AudioSegment.from_mp3("/home/ulan/Music/Europa1.mp3")

	# pydub does things in miliseconds
	ten_minutes = 0.5 * 60 * 1000
	one_minute = 1 * 60 * 1000
	half_minute = 30 * 1000

	length = len(segment)

	ten_parts = length/ten_minutes

	for i in range(ten_parts):
		part = segment[i*ten_minutes:(i+1)*ten_minutes]
		part.export(str(i)+".mp3", format="mp3")
    	'''
	for filename in glob('/home/ulan/PyMusic/*.mp3'):
       		process_file(filename,conn)
	
	conn.close()	
