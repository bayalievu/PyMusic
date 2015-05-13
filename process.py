import MySQLdb
import sys
import os
import subprocess32
from transliterate import translit
from glob import glob
import simplejson as json
workspace = "/home/monitor/Workspace/"
sys.path.insert(0, workspace + "echoprint-server/API")
import fp

codegen_path = os.path.abspath(workspace+"echoprint-codegen/echoprint-codegen")

artists = {}

def codegen(file):
    proclist = [codegen_path, os.path.abspath(file)]
    p = subprocess32.Popen(proclist, stdout=subprocess32.PIPE)
    code = p.communicate()[0]
    return json.loads(code)

def parse_json(c):
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

def process_file(absoluteFilename,c):
	#Get filename from absolute path
	filename = absoluteFilename.split('/')[-1].split("-")	
	#Get artists from filename
	artist=filename[0].strip()
	song = ""
        logfile.write(absoluteFilename+'\n')
	#Get song name from filename
	if len(filename) > 1:
		song = filename[1].split(".")[0].strip()

	#Add artists to Database
	artists_id=addArtistToDb(artist)
	
	#Get track id
	code = parse_json(c[0])	
	track_id =code["track_id"]

	db = conn.cursor()
	try:
		#Insert into melody table
	   	db.execute("""INSERT INTO melody(track_id,artist,song,filename) VALUES (%s,%s,%s,%s)""",(track_id,artist,song,absoluteFilename))
	   	logfile.write("Inserted track to database "+track_id+'\n')
	   	conn.commit()
		insertArtistMelodyLink(artists_id,db.lastrowid)
		
		#Save fingerprint in Solr
		fp.ingest(code, do_commit=False)
    		fp.commit()
	except db.Error, e:
           	logfile.write("Error %d: %s" % (e.args[0],e.args[1]))
	   	conn.rollback()
	
	db.close()

def insertArtistMelodyLink(artists_id,melody_id):
	db = conn.cursor()
	for a in artists_id:
                try:
                        db.execute("""INSERT INTO artist_melody(artist_id,melody_id) VALUES (%s,%s)""",(a,melody_id))
                        logfile.write("Inserted artist_melody link "+str(a)+""+str(melody_id)+'\n')
                        conn.commit()
                except db.Error, e:
                        logfile.write("Error %d: %s" % (e.args[0],e.args[1]))
                        conn.rollback()
	db.close()


def addArtistToDb(artist):
	db = conn.cursor()
	a = artist.split('_')
	ids=[]
	for x in a:
		s = x.strip().decode("utf-8")	
		if not s in artists.keys():
                	try:
                        	db.execute("""INSERT INTO artist(name) VALUES (%s)""",(s,))
                        	logfile.write("Inserted artist to database "+x+'\n')
                        	conn.commit()
				artist_id = db.lastrowid
				artists[s]=artist_id
				ids.append(artist_id)
                	except db.Error, e:
                        	logfile.write("Error %d: %s" % (e.args[0],e.args[1]))
                        	conn.rollback()
		else:
			ids.append(artists[s])	
	db.close()
	return ids

def getArtists():
        db = conn.cursor()

        sql = "SELECT * FROM artist"

        try:
                db.execute(sql)
                # Fetch all the rows in a list of lists.
                results = db.fetchall()
                for row in results:
			i = row[0]
                        a = row[1].strip()
                        artists[a]=i
	except db.Error, e:
        	logfile.write("Error %d: %s" % (e.args[0],e.args[1]))
	
	db.close()

#Check is melody fingerprint is already in Solr
def melodyExists(filename,c):
	decoded = fp.decode_code_string(c[0]["code"])
        result = fp.best_match_for_query(decoded)
        if result.TRID:
		logfile.write(filename+" is already in the database\n")
        	return True
	else:
		return False

def getNowDateTime():
       import time
       return time.strftime('%Y-%m-%d %H:%M:%S')
	
if __name__ == "__main__":
	if len(sys.argv) < 2:
        	print "Usage: python process.py mp3path"
                exit()

	conn = MySQLdb.connect(host= "localhost",user="root", passwd="ulut123", db="pymusic",charset='utf8')
	getArtists()
	
        mp3path = sys.argv[1]
	
	# Open logfile
	logfile = open(workspace+'PyMusic/logs/logfileProcess'+getNowDateTime(), 'w', 1)
	
	files = glob(mp3path)
	files.sort()
    	for filename in files:
		c=codegen(filename)
        	if c is None or len(c)==0 or "code" not in c[0]:
			logfile.write("No code is generated for: " + filename+'\n')
			continue
 		#Add melody if it does not already exists
		if not melodyExists(filename,c):
       			process_file(filename,c)

	conn.close()	
	logfile.close()
