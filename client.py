import os
import subprocess
import time    
import sys
import time

codegen_path = os.path.abspath("/home/server/echoprint-codegen/echoprint-codegen")

try:
    import json
except ImportError:
    import simplejson as json


def codegen(file, start=0, duration=30):
    	proclist = [codegen_path, os.path.abspath(file), "%d" % start, "%d" % duration]
    	p = subprocess.Popen(proclist, stdout=subprocess.PIPE)                      
    	code = p.communicate()[0]                                                   
    	return json.loads(code)

def process_file(filename,radio):
    	codes = codegen(filename)
	fp_code = None
    	if len(codes) and "code" in codes[0]:
		fp_code = codes[0]["code"]
		import requests
		url = "http://192.168.1.100:8080/identify?fp_code="+fp_code+"&radio="+radio
		try:
			data = requests.get(url).json
		except requests.ConnectionError:
			#If there is no connection the server
			#Write fingerprint to DB for future processing
		        print "No connection to the server"
			#db = conn.cursor()
			try:
				now = time.strftime('%Y-%m-%d %H:%M:%S')
	   			#db.execute("""INSERT INTO unchecked_melody(fingerprint,radio,time_played) VALUES (%s,%s,%s)""",(fp_code,radio,now))
	   			print("""INSERT INTO unchecked_melody(fingerprint,radio,time_played) VALUES (%s,%s,%s)""",(fp_code,radio,now))
	   			#conn.commit()
			except db.Error, e:
           			print "Error %d: %s" % (e.args[0],e.args[1])
	   			conn.rollback()
	
		
	else:
		print "No code generated for file "+ filename

if __name__ == "__main__":
	
	if len(sys.argv) < 3:
		print "Usage: python client.py radio soundcard"
		exit()
	
	#conn = MySQLdb.connect(host= "localhost",user="root", passwd="1qaz", db="pymusic",charset='utf8')	
	radio = sys.argv[1]
	soundcard = sys.argv[2]
	import alsaaudio, wave, numpy
	card_info = {}
	for device_number, card_name in enumerate(alsaaudio.cards()):
    		card_info[card_name] = "hw:%s,0" % device_number
	
	#CMI8738, CMI8738_1, PCH
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,card=card_info[soundcard])
	inp.setchannels(2)
	inp.setrate(44100)
	inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	inp.setperiodsize(1024)

	while True:
		now = time.strftime('%Y-%m-%d %H:%M:%S')
		filename = radio+now+'.wav'	
		w = wave.open(filename, 'w')
		w.setnchannels(2)
		w.setsampwidth(2)
		w.setframerate(44100)
		#Record 30 seconds and recognize
    		for i in range(int(30*44.1)):
			l, data = inp.read()
			
			try:
    				a = numpy.fromstring(data, dtype='int16')
			except ValueError:
				print "Input could NOT be read, ignoring 1/44100 seconds data"

    			w.writeframes(data)
		process_file(filename,radio)	




