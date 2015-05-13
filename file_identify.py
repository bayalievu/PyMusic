workspace = "/home/monitor/Workspace/"
import sys
sys.path.insert(0, workspace +"echoprint-server/API")
import MySQLdb
import os
import subprocess32
import time    
from glob import glob
import fp
from pydub import AudioSegment

codegen_path = os.path.abspath(workspace+"echoprint-codegen/echoprint-codegen")

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

        decoded = fp.decode_code_string(codes[0]["code"])
        result = fp.best_match_for_query(decoded)
        if result.TRID:
		print result.TRID
		
		
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
                print "Usage: python file_identify.py radio radio_id filename"
                exit()

        radio = sys.argv[1]
	radio_id = sys.argv[2]
        filename = sys.argv[3]

	logfile = open(workspace+"PyMusic/logs/"+radio+"LogFileIdentify"+getNowDateTime(), 'w',1)
        
	try:
        	segment = AudioSegment.from_mp3(filename)

        	# pydub does things in miliseconds
        	one_minute =  40 * 1000
        	length = len(segment)
        	parts = length/one_minute

        	for i in range(parts):
                	part = segment[i*one_minute:(i+1)*one_minute]
                	part.export(workspace+"PyMusic/mp3/"+"%09d"%i+".mp3", format="mp3",bitrate="80k")


        	# Process files sorted by modified time
        	files = sorted(glob(workspace+'PyMusic/mp3/*.mp3'))
        	print "Number of files: "+ str(len(files))
        	for filename in files:
                	process_file(filename)
	
	except KeyboardInterrupt:
		logfile.close()
		exit()
