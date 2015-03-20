import sys
sys.path.insert(0, "/home/ulan/echoprint-server/API")
import MySQLdb
import os
import time    
import fp

def reprocess(fid,decoded,date_played,time_played,radio,radio_id):

        result = fp.best_match_for_query(decoded)
        if result.TRID:
		#Melody is recognized
		track_id = result.TRID
		current = convertTimeToMinutes(time_played)
		global last_time,last_radio
		try:
			now = time.strftime('%Y-%m-%d %H:%M:%S')
			#Insert only tracks which differ more than 5 minutes, it is do to prevent repeated insert from different parts of the same track
			if (last_radio is None) or (last_radio != radio_id) or (last_time == 0) or (current - last_time > 5):
				last_time=current
				last_radio=radio_id 
			
				db = conn.cursor()    	
	   			logfile.write("Inserting track_id: " + track_id	+ " for fingerprint " +str(fid)+'\n')
	   			db.execute("""INSERT INTO played_melody(track_id,radio,date_played,time_played,radio_id) VALUES (%s,%s,%s,%s,%s)""",(track_id,radio,date_played,time_played,radio_id))
	   			conn.commit()
				db.close()
				
				db = conn.cursor()    	
	   			logfile.write("Updating fingerprint " +str(fid)+ " as "+track_id +'\n')
				db.execute("""update fingerprint set status = 'Y', track_id = %s, time_identified=%s  where id = %s""",(track_id,now,fid))
	   			conn.commit()
				db.close()
			else:			
				logfile.write("Track is already recognized from previous fingerprint "+radio+str(date_played)+":"+str(time_played)+'\n')
				db = conn.cursor()    	
	   			logfile.write("Updating fingerprint " +str(fid)+ " as Y" +'\n')
				db.execute("""update fingerprint set status = 'Y', time_identified=%s  where id = %s""",(now,fid))
	   			conn.commit()
				db.close()
		
		except db.Error, e:
                	logfile.write("Error %d: %s\n" % (e.args[0],e.args[1]))
                        conn.rollback()			

	return 0
		
def convertTimeToMinutes(t):
	(h, m, s) = str(t).split(':')
	result = int(h) * 60 + int(m)
	return result

if __name__ == "__main__":
	print time.strftime('%Y-%m-%d %H:%M:%S')
 	if len(sys.argv) < 2:
                print "Usage: python reprocess.py date(YYYY-mm-dd)"
                exit()

        last_time=0
	last_radio=None
        when = sys.argv[1]

        conn = MySQLdb.connect(host= "192.168.3.111",user="root", passwd="123", db="pymusic",charset='utf8')
	db = conn.cursor()

        try:
		logfile = open("logs/reprocess"+time.strftime('%Y-%m-%d %H:%M:%S'), 'w')
                
		db.execute("""SELECT * FROM fingerprint where status='N' and date_played=%s order by radio_id,time_played""",(when,))
                # Fetch all the rows in a list of lists.
                results = db.fetchall()
                for row in results:
			fid = row[0]
			decoded = row[1]
			radio = row[2]
			date_played = row[3]
			time_played = row[4]
			radio_id = row[7]
			reprocess(fid,decoded,date_played,time_played,radio,radio_id)
			'''
			| id              | int(11)        | NO   | PRI | NULL    | auto_increment |
			| fp              | varchar(32000) | YES  |     | NULL    |                |
			| radio           | varchar(255)   | YES  | MUL | NULL    |                |
			| date_played     | date           | YES  | MUL | NULL    |                |
			| time_played     | time           | YES  | MUL | NULL    |                |
			| time_identified | datetime       | YES  |     | NULL    |                |
			| status          | char(1)        | YES  |     | NULL    |                |
			| radio_id        | int(11)        | YES  | MUL | NULL    |                |
			| track_id        | varchar(255)   | YES  | MUL | NULL    |                |
			'''
        except db.Error, e:
                logfile.write("Error %d: %s" % (e.args[0],e.args[1]))
		db.close()
	except KeyboardInterrupt:
		logfile.write("Program was interrupted using keyboard"+'\n')
        	db.close()
		logfile.close()
		conn.close()	
		exit()
	
	db.close()
	logfile.close()
	conn.close()	
	print	time.strftime('%Y-%m-%d %H:%M:%S')
	exit()

