if __name__ == "__main__":
        import MySQLdb
        #Delete melodies from DB
	conn = MySQLdb.connect(host= "localhost",user="root", passwd="123", db="pymusic",charset='utf8')
        db = conn.cursor()
        try:
           db.execute("""delete from melody""")
           db.execute("""delete from played_melody""")
           conn.commit()
        except db.Error, e:
           print "Error %d: %s" % (e.args[0],e.args[1])
           conn.rollback()
        conn.close()    

	#Delete melodies from solr
	import requests
	url = "http://localhost:8502/solr/fp/update?stream.body=%3Cdelete%3E%3Cquery%3E*:*%3C/query%3E%3C/delete%3E"
	data = requests.get(url).json
	print data	
	
	url = "http://localhost:8502/solr/fp/update?stream.body=%3Ccommit/%3E"
	data = requests.get(url).json
	print data	
