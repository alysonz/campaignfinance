#!/usr/bin/python
#import resources
import cgi
import cgitb
import json
from cfstorm import *

def log(message):
	file = open("/var/log/apache2/alyson.log","a")
	file.write(message)
	file.write("\n")
	file.close()

report = 0

#get form variables
form = cgi.FieldStorage()

download = form.getvalue('download', False)
if download:
	download = cgi.escape(download)

committeeID = form.getlist('committeeID')
for committee in committeeID:
	if committee:
		committee = cgi.escape(committee)

entityOneType = form.getvalue('entityOneType', False)
if entityOneType:
	entityOneType = cgi.escape(entityOneType)

entityOneFirstName = form.getvalue('entityOneFirstName','')
if entityOneFirstName:
	entityOneFirstName= cgi.escape(entityOneFirstName)

entityOneLastName = form.getvalue('entityOneLastName','')
if entityOneLastName:
	entityOneLastName = cgi.escape(entityOneLastName)

cycleName = form.getvalue('cycleName' ,False)
if cycleName:
	cycleName = cgi.escape(cycleName)


#get report
if committeeID:
	report = committeeQuery(committeeID, cycleName, download)
else:
	report = individualQuery(entityOneLastName, entityOneFirstName)
	if cycleName != "All":
		report = cycle(cycleName, report)
#filter
#if cycleName != "All":
#	report = cycle(cycleName, report)

#finalize
report = convertDate(report)

#begin web content
if (download):
	download = "data.csv"
	print "content-type:text/csv"
	print "Content-disposition: attachment;filename=%s"%(download)
	print
	#print contents of report
	for line in report[0]['transactions']:
		line = [str(x) for x in line]
		line = "|".join(line)
		line = line.rstrip()
		print line
else:
	print 'Content-Type: application/json\n\n'
	print
	#print contents of report
	print json.dumps(report)
