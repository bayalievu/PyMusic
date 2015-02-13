
import MySQLdb
import sys
import os
import subprocess
from transliterate import translit
from glob import glob
try:
    import json
except ImportError:
    import simplejson as json

sys.path.insert(0, "/home/ulan/echoprint-server/API")
import fp

codegen_path = os.path.abspath("/home/ulan/echoprint-codegen/echoprint-codegen")

def codegen(file):
    proclist = [codegen_path, os.path.abspath(file)]
    p = subprocess.Popen(proclist, stdout=subprocess.PIPE)
    code = p.communicate()[0]
    return json.loads(code)

def parse_json(j):
	c = j[0]

        if "code" not in c:
            return None
        code = c["code"]
        m = c["metadata"]
        if "track_id" in m:
            trid = m["track_id"].encode("utf-8")
        else:
            trid = fp.new_track_id()
        length = m["duration"]
        version = m["version"]
        artist = m.get("artist", None)
        title = m.get("title", None)
        release = m.get("release", None)
        decoded = fp.decode_code_string(code)

        data = {"track_id": trid,
            "fp": decoded,
            "length": length,
            "codever": "%.2f" % version
        }

        if artist: data["artist"] = artist
        if release: data["release"] = release
        if title: data["track"] = title

    	return data

def process_file(filename,conn,logfile):
	cyrillic_filename = filename
	#Convert latin to to cyrillic
	try:
    		filename.decode('ascii')
	except UnicodeDecodeError:
		cyrillic_filename = filename
	else:
		cyrillic_filename = translit(filename,'ru')
		
	
	s = cyrillic_filename.split('/')[-1].split("-")	
	artist=s[0]
	song = ""
        logfile.write(filename+'\n')
	print filename
	if len(s) > 1:
		song = s[1].split(".")[0]
	
	c=codegen(filename)
	
	code = parse_json(c)
	if code is None:
		logfile.write("No code is generated for: " + filename+'\n')
		return
	
	track_id =code["track_id"]
        
	
	fp.ingest(code, do_commit=False)
    	fp.commit()

	db = conn.cursor()
	try:
	   db.execute("""INSERT INTO melody(track_id,artist,song,filename) VALUES (%s,%s,%s,%s)""",(track_id,artist,song,filename))
	   logfile.write("Inserted track to database "+track_id+'\n')
	   conn.commit()
	except db.Error, e:
           logfile.write("Error %d: %s" % (e.args[0],e.args[1]))
	   conn.rollback()
	

if __name__ == "__main__":
	conn = MySQLdb.connect(host= "localhost",user="root", passwd="123", db="pymusic",charset='utf8')
	
	# Open logfile
	logfile = open('logfile', 'w')

	files = glob('/home/ulan/Music/radio_songs/*.mp3')
	files.sort()
    	for filename in files:
       		process_file(filename,conn,logfile)
	
	files = glob('/home/ulan/Music/Testmp3/mp3/*.wav')
	files.sort()
	for filename in files:
       		process_file(filename,conn,logfile)

	conn.close()	
	logfile.close()
