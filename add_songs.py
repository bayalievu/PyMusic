import MySQLdb
import sys
import os
import subprocess32
from transliterate import translit
from glob import glob
import simplejson as json

sys.path.insert(0, "/home/monitor/Workspace/echoprint-server/API")
import fp

codegen_path = os.path.abspath("/home/monitor/Workspace/echoprint-codegen/echoprint-codegen")

def getNowDateTime():
       import time
       return time.strftime('%Y-%m-%d %H:%M:%S')       

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

def process_file(path,c,mid,song):
	artists_id=getArtistsFromUploadedMelody(mid)
	if artists_id is None:
		return
	
	#Get track id
	code = parse_json(c[0])	
	track_id =code["track_id"]
	
	conn = MySQLdb.connect(host= "localhost",user="root", passwd="ulut123", db="pymusic",charset='utf8')
	db = conn.cursor()
	try:
		#Insert into melody table
	   	db.execute("""INSERT INTO melody(track_id,artist,song,filename) VALUES (%s,%s,%s,%s)""",(track_id,"",song,path))
	   	logfile.write("Inserted track to database "+track_id+'\n')
	   	conn.commit()
		insertArtistMelodyLink(artists_id,db.lastrowid)
		
		#Save fingerprint in Solr
		fp.ingest(code, do_commit=False)
    		fp.commit()
	except db.Error, e:
           	logfile.write("Error %d: %s" % (e.args[0],e.args[1]))
		updateUploadedMelodyError("Could not insert artist or  melody table Error %d: %s" % (e.args[0],e.args[1]),mid,1,0)	
		conn.rollback()

	db.close()
	conn.close()

def insertArtistMelodyLink(artists_id,melody_id):
	conn = MySQLdb.connect(host= "localhost",user="root", passwd="ulut123", db="pymusic",charset='utf8')
	db = conn.cursor()
	for a in artists_id:
                try:
                        db.execute("""INSERT INTO artist_melody(artist_id,melody_id) VALUES (%s,%s)""",(a,melody_id))
                        logfile.write("Inserted artist_melody link "+str(a)+""+str(melody_id)+'\n')
                        conn.commit()
                except db.Error, e:
			raise
	db.close()
	conn.close()

def getArtistsFromUploadedMelody(mid):
	artists = []
	conn = MySQLdb.connect(host= "localhost",user="root", passwd="ulut123", db="pymusic",charset='utf8')
        db = conn.cursor()

        try:
                db.execute("""SELECT * FROM uploaded_artist_melody where melody_id = %s""",(mid,))
                results = db.fetchall()
                for row in results:
                        a = row[1]
                        artists.append(a)
	except db.Error, e:
        	logfile.write("Error %d: %s" % (e.args[0],e.args[1]))
		updateUploadedMelodyError("Error in getArtistsFromUploaded Melody %d: %s" % (e.args[0],e.args[1]),mid,1,0)
		return None		
	
	db.close()
	conn.close()
	return artists

#Check is melody fingerprint is already in Solr
def melodyExists(filename,c):
	decoded = fp.decode_code_string(c[0]["code"])
        result = fp.best_match_for_query(decoded)
        if result.TRID:
		logfile.write(filename+" is already in the database\n")
        	return True
	else:
		return False

def updateUploadedMelodyError(error,mid,declined_status,added_status):
        conn = MySQLdb.connect(host= "localhost",user="root", passwd="ulut123", db="pymusic",charset='utf8')
        db = conn.cursor()
                
	try:
        	db.execute("""update uploaded_song set melody_declined_error = %s,melody_declined_flag=%s,melody_added_flag=%s where id = %s """,(error,declined_status,added_status,mid))
                logfile.write("Update upploaded_song error and status:"+str(mid)+"\n")
                conn.commit()
        except db.Error, e:
        	raise
        
	db.close()
        conn.close()
	
	
if __name__ == "__main__":
	# Open connection
	connection = MySQLdb.connect(host= "localhost",user="root", passwd="ulut123", db="pymusic",charset='utf8')
		
	# Open logfile
	logfile = open('/home/monitor/Workspace/PyMusic/logs/uploadLogfile'+getNowDateTime(), 'w', 1)

	cursor = connection.cursor()

        sql = "select id,filename,song_name from uploaded_song where approved_flag = 1 and melody_added_flag = 0 and melody_declined_flag = 0"
	files_added = 0
        try:
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                        mid = row[0]
                        filename = row[1].strip()
			song = row[2].strip()
                	c=codegen(filename)
                	if c is None or len(c)==0 or "code" not in c[0]:
                        	logfile.write("No code is generated for: " + filename+'\n')
				updateUploadedMelodyError("File is corrupted, no fingerprint could be generated",mid,1,0)
                        	continue
                	#Add melody if it does not already exists
			if not melodyExists(filename,c):
                        	process_file(filename,c,mid,song)
				updateUploadedMelodyError("Melody successfully added",mid,0,1)
				files_added = files_added + 1
			else:
				updateUploadedMelodyError("Melody already exists in Database",mid,1,0)
        except cursor.Error, e:
                logfile.write("Error %d: %s" % (e.args[0],e.args[1]))	

	logfile.write("Number of melodies added:"+str(files_added))
        cursor.close()
	connection.close()	
	logfile.close()