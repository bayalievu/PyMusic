import sys
sys.path.insert(0, "/home/monitor/Workspace/echoprint-server/API")
import MySQLdb
import os
import time    
import fp

def reprocess(fid,decoded,date_played,time_played,radio,radio_id):

        result = fp.best_match_for_query(decoded)
        if result.TRID:
		logfile.write("Melody is recognized: "+result.TRID+",")
		#Melody is recognized
		track_id = result.TRID
		current = convertTimeToMinutes(time_played)
		global last_time,last_radio,recognized
		try:
			#Insert only tracks which differ more than 5 minutes, it is do to prevent repeated insert from different parts of the same track
			if (last_radio is None) or (last_radio != radio_id) or (last_time == 0) or (current - last_time > 5):
				last_time=current
				last_radio=radio_id 
				recognized = recognized + 1
			
				db = conn.cursor()    	
	   			logfile.write("Inserting track_id: " + track_id	+ " for fingerprint " +str(fid)+'\n')
	   			db.execute("""INSERT INTO played_melody(track_id,radio,date_played,time_played,radio_id) VALUES (%s,%s,%s,%s,%s)""",(track_id,radio,date_played,time_played,radio_id))
	   			conn.commit()
				db.close()
				
				db = conn.cursor()    	
	   			logfile.write("Updating fingerprint " +str(fid)+ " as "+track_id +'\n')
				db.execute("""update fingerprint set status = 'Y', track_id = %s, time_identified=%s  where id = %s""",(track_id,getNowDateTime(),fid))
	   			conn.commit()
				db.close()
			else:			
				logfile.write("Track is already recognized from previous fingerprint "+radio+str(date_played)+":"+str(time_played)+'\n')
				db = conn.cursor()    	
	   			logfile.write("Updating fingerprint " +str(fid)+ " as Y" +'\n')
				db.execute("""update fingerprint set status = 'Y', time_identified=%s  where id = %s""",(getNowDateTime(),fid))
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

def getNowTime():
	return time.strftime('%H:%M:%S')

def getNowDate():
	return time.strftime('%Y-%m-%d')
		
def getNowDateTime():
	return time.strftime('%Y-%m-%d %H:%M:%S')	


if __name__ == "__main__":
 	if len(sys.argv) < 3:
                print "Usage: python reprocess.py startDate(YYYY-mm-DD) endDate(YYYY-mm-DD)"
                exit()

	logfile = open("logs/reprocess"+getNowDateTime(), 'w',1)
	logfile.write(getNowDateTime()+'\n')
        last_time=0
	recognized = 0
	last_radio=None
        startDate = sys.argv[1]
	endDate = sys.argv[2]
	

        conn = MySQLdb.connect(host= "localhost",user="root", passwd="ulut123", db="pymusic",charset='utf8')
	db = conn.cursor()

        try:
                
		db.execute("""SELECT * FROM fingerprint where status='N' and date_played>=%s and date_played<=%s order by radio_id,time_played""",(startDate,endDate))

		logfile.write(db._executed+'\n')
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
        except db.Error, e:
                logfile.write("Error %d: %s" % (e.args[0],e.args[1]))
		db.close()
		logfile.close()
		conn.close()	
	except KeyboardInterrupt:
		logfile.write("Program was interrupted using keyboard"+'\n')
        	db.close()
		logfile.close()
		conn.close()	
		exit()
	
	logfile.write(getNowDateTime()+'\n')
	logfile.write("Songs recognized: " + str(recognized)+'\n')
	db.close()
	logfile.close()
	conn.close()	
        exit()	
