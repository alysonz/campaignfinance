# General query tools
import MySQLdb
import re
db = MySQLdb.connect(user='alyson', passwd='thetempleofwhollyness', db='campaignfinance')
cursor= db.cursor()
genericVariable = "you misspelled something somewhere"
genericList = []
#create table to load data
cursor.execute("create table ballotMeasures (ballotMeasureID int(5), sosIdentifier varchar (15), measureNumber int(5), shortTitle varchar(100), officialTitle varchar(500)")
#find all distinct departments
cursor.execute("select generic from generic where generic=generic")
for line in cursor:
	generic = line
	#for each distinct department, find all distinct titles
	cursor.execute("select generic from generic where generic=%s;" , (generic[0]))
	generic = cursor.fetchall()
	genericList.extend(['generic',generic[0]])
	cursor.execute("insert into generic (generic1, generic2, generic3) values(%s, %s, %s)" ,(genericList[0], genericList[1], genericList[2]))
		#clear lists for next job title analysis
		genericList = []
#write to heshenames database
db.commit()
print 'Success!'
cursor.close()
db.close()
