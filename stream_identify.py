import sys
sys.path.insert(0, "/home/monitor/Workspace/echoprint-server/API")
import MySQLdb
import os
import subprocess32
import time    
from glob import glob
import fp

codegen_path = os.path.abspath("/home/monitor/Workspace/echoprint-codegen/echoprint-codegen")

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

def process_file(filename):

	codes = codegen(filename)
	if codes is None:
		return -2
	if len(codes) == 0:
		logfile.write("Codegen returned empty list"+"\n")
		return -3
	if "code" not in codes[0]:
		logfile.write("No code is returned by codegen"+"\n")
		return -4

	now_time = time.strftime('%H:%M:%S')
	now_date = time.strftime('%Y-%m-%d')
	db = conn.cursor()    	
	track_id = None
	
        decoded = fp.decode_code_string(codes[0]["code"])
        result = fp.best_match_for_query(decoded)
        if result.TRID:
		#Melody is recognized
		track_id = result.TRID
		global last
		#Insert tracks only once
		if (last == 0) or (last != track_id):
			last=track_id

			try:
	   			logfile.write("Inserting track_id: " + track_id	+ " for file: " + filename+'\n')
	   			db.execute("""INSERT INTO played_melody(track_id,radio,date_played,time_played,radio_id) VALUES (%s,%s,%s,%s,%s)""",(track_id,radio,now_date,now_time,radio_id))
	   			conn.commit()
			except db.Error, e:
           			logfile.write("Error %d: %s\n" % (e.args[0],e.args[1]))
	   			conn.rollback()
		else:
			logfile.write("Track is already recognized from other file "+filename+'\n')

		db.close()	
		return 0
	else:
		#Insert unknown fingerprints with status 'N'
		logfile.write("No match found for the file, inserting unknown melody to fingerprint table"+'\n')
                db.execute("""INSERT INTO fingerprint(fp,radio,date_played,time_played,time_identified,status,radio_id,track_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(decoded,radio,now_date,now_time,None,'N',radio_id,None))
                conn.commit()		
		db.close()	
		return -1
		
	

if __name__ == "__main__":
 	import urllib2
        from datetime import datetime
        from datetime import timedelta
       
	if len(sys.argv) < 4:
                print "Usage: python stream_identify.py radio radio_id stream"
                exit()

	last=0
        radio = sys.argv[1]
	radio_id = sys.argv[2]
        stream = sys.argv[3]

	logfile = open("/home/monitor/Workspace/PyMusic/logs/radio"+radio+"logStreamIdentify"+time.strftime('%Y-%m-%d %H:%M:%S'), 'w',1)
   	url=urllib2.urlopen(stream)
        conn = MySQLdb.connect(host= "localhost",user="root", passwd="ulut123", db="pymusic",charset='utf8')
        
	try:	
		while True:
	        	now = time.strftime('%Y-%m-%d %H:%M:%S')
                	filename = "/home/monitor/Workspace/PyMusic/wavs/"+radio+now+'.mp3'
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

			result = process_file(filename) 
			os.remove(filename)
		
	except KeyboardInterrupt:
		logfile.close()
		conn.close()	
		url.close()
		f.close()
		exit()
