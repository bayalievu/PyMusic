import sys
sys.path.insert(0, "/home/ulan/echoprint-server/API")
import MySQLdb
import os
import subprocess32
import time    
from glob import glob
import fp
from pydub import AudioSegment

codegen_path = os.path.abspath("/home/ulan/echoprint-codegen/echoprint-codegen")

import simplejson as json
import simplejson.scanner


def codegen(file, start=0, duration=40):
    	proclist = [codegen_path, os.path.abspath(file), "%d" % start, "%d" % duration]
    	p = subprocess32.Popen(proclist, stdout=subprocess32.PIPE)                      
    	r = p.communicate()
	
	try:
		code = json.loads(r[0])
	except simplejson.scanner.JSONDecodeError:
		logfile.write(getNowDateTime()+":Json cannot be decoded "+str(r[0])+"\n")
		return None
    	
	return code

def process_file(filename):

	codes = codegen(filename)
	if codes is None:
		return -2
	if len(codes) == 0:
		logfile.write(getNowDateTime()+":Codegen returned empty list\n")
		return -3
	if "code" not in codes[0]:
		logfile.write(getNowDateTime()+":No code is returned by codegen\n")
		return -4

	db = conn.cursor()    	
	track_id = None
	
        decoded = fp.decode_code_string(codes[0]["code"])
        result = fp.best_match_for_query(decoded)
        if result.TRID:
		#Melody is recognized
		track_id = result.TRID
		global last
		#Insert tracks which were identified at least twice and insert track only once
		if last is None or (last != track_id):
			last=track_id

			try:
	   			logfile.write(getNowDateTime()+":Inserting track_id: " + track_id	+ " for file: " + filename+'\n')
	   			db.execute("""INSERT INTO played_melody(track_id,radio,date_played,time_played,radio_id) VALUES (%s,%s,%s,%s,%s)""",(track_id,radio,getNowDate(),getNowTime(),radio_id))
	   			conn.commit()
			except db.Error, e:
				logfile.write(getNowDateTime())
           			logfile.write(":Error %d: %s\n" % (e.args[0],e.args[1]))
	   			conn.rollback()
		else:
			logfile.write(getNowDateTime()+":Track "+track_id+" is already recognized from other file\n")

		db.close()	
		return 0
	else:
		#Insert unknown fingerprints with status 'N'
		logfile.write(getNowDateTime()+":No match found for the file, inserting unknown melody to fingerprint table\n")
                db.execute("""INSERT INTO fingerprint(fp,radio,date_played,time_played,time_identified,status,radio_id,track_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(decoded,radio,getNowDate(),getNowTime(),None,'N',radio_id,None))
                conn.commit()		
		db.close()	
		return -1

def getNowTime():
	return time.strftime('%H:%M:%S')

def getNowDate():
	return time.strftime('%Y-%m-%d')
		
def getNowDateTime():
	return time.strftime('%Y-%m-%d %H:%M:%S')	

if __name__ == "__main__":
	import collections
 	import urllib2
        from datetime import datetime
        from datetime import timedelta
       
	if len(sys.argv) < 4:
                print "Usage: python stream_identify.py radio radio_id filename"
                exit()

	last=None
        radio = sys.argv[1]
	radio_id = sys.argv[2]
        filename = sys.argv[3]

	logfile = open("/home/ulan/PyMusic/logs/"+radio+"LogFileIdentify"+getNowDateTime(), 'w',1)
        conn = MySQLdb.connect(host= "localhost",user="root", passwd="123", db="pymusic",charset='utf8')
        
	try:
        	segment = AudioSegment.from_mp3(filename)

        	# pydub does things in miliseconds
        	one_minute =  40 * 1000
        	length = len(segment)
        	parts = length/one_minute

        	for i in range(parts):
                	part = segment[i*one_minute:(i+1)*one_minute]
                	part.export("/home/ulan/PyMusic/mp3/"+"%09d"%i+".mp3", format="mp3",bitrate="80k")


        	# Process files sorted by modified time
        	files = sorted(glob('/home/ulan/PyMusic/mp3/*.mp3'))
        	print "Number of files: "+ str(len(files))
        	for filename in files:
                	process_file(filename)
	
	except KeyboardInterrupt:
		logfile.close()
		conn.close()	
		f.close()
		exit()
