from pydub import AudioSegment
import sys
sys.path.insert(0, "/home/ulan/echoprint-server/API")
import MySQLdb
import os
import subprocess32
import time    
from glob import glob
import fp

last=0
codegen_path = os.path.abspath("/home/ulan/echoprint-codegen/echoprint-codegen")

import simplejson as json
import simplejson.scanner


def codegen(file, start=0, duration=30):
    	proclist = [codegen_path, os.path.abspath(file), "%d" % start, "%d" % duration]
    	p = subprocess32.Popen(proclist, stdout=subprocess32.PIPE)                      
    	r = p.communicate()
	
	try:
		code = json.loads(r[0])
	except simplejson.scanner.JSONDecodeError:
		logfile.write("Json cannot be decoded "+str(r[0])+"\n")
		return None
    	
	return code

def process_file(filename,radio):

	codes = codegen(filename)
	if codes is None:
		return -2

	now_time = time.strftime('%H:%M:%S')
	now_date = time.strftime('%Y-%m-%d')
	db = conn.cursor()    	
	track_id = None
	
    	if len(codes)>0 and "code" in codes[0]:
        	decoded = fp.decode_code_string(codes[0]["code"])
        	result = fp.best_match_for_query(decoded)
        	if result.TRID:
			track_id = result.TRID
		else:
			#Insert melody to unknown fingerprints table with status 'N'
			logfile.write("No match found for the file, inserting unknown melody to fingerprint table"+'\n')
                        db.execute("""INSERT INTO fingerprint(fp,radio,date_played,time_played,time_identified,status) VALUES (%s,%s,%s,%s,%s,%s)""",(decoded,radio,now_date,now_time,None,'N'))
                        conn.commit()		
			db.close()	
			return -1
		
	global last
	#Insert tracks only once
	if (last == 0) or (last != track_id):
		last=track_id

		try:
	   		logfile.write("Inserting track_id: " + track_id	+ " for file: " + filename+'\n')
	   		db.execute("""INSERT INTO played_melody(track_id,radio,date_played,time_played) VALUES (%s,%s,%s,%s)""",(track_id,radio,now_date,now_time))
	   		conn.commit()
		except db.Error, e:
           		logfile.write("Error %d: %s\n" % (e.args[0],e.args[1]))
	   		conn.rollback()
	else:
		logfile.write("Track is already recognized from other file "+filename+'\n')
	
	db.close()
	
	return 0

if __name__ == "__main__":
 	import urllib2
        from datetime import datetime
        from datetime import timedelta
       
	if len(sys.argv) < 3:
                print "Usage: python stream_identify.py radio stream"
                exit()

        radio = sys.argv[1]
        stream = sys.argv[2]

   	url=urllib2.urlopen(stream)
        conn = MySQLdb.connect(host= "192.168.3.111",user="root", passwd="123", db="pymusic",charset='utf8')
        

	logfile = open('logfileStreamIdentify'+radio+time.strftime('%Y-%m-%d %H:%M:%S'), 'w')
        last_result = -1
	try:	
		while True:
	        	now = time.strftime('%Y-%m-%d %H:%M:%S')
                	filename = "wavs/"+radio+now+'.mp3'
                	f=file(filename, 'wb')

                	# Basically a timer
                	t_start = datetime.now()
                	t_end = datetime.now()
                	t_end_old = t_end

                	# Record in chunks until
                	while t_end-t_start < timedelta(seconds=30):
                        	f.write(url.read(1024))
                        	t_end = datetime.now()
                	f.close()

			result = process_file(filename,radio) 
			os.remove(filename)
		'''
		if result == 0 or last_result == 0:
			os.remove(filename)
		last_result = result
		'''
	except KeyboardInterrupt:
		logfile.close()
		conn.close()	
		url.close()
		f.close()
		exit()
