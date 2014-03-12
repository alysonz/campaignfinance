#!/usr/bin/python
#import resources
import cgi
import cgitb
import cfquery
import json
def log(message):
	file = open("/var/log/apache2/alyson.log","a")
	file.write(message)
	file.write("\n")
	file.close()

#get form variables
form = cgi.FieldStorage()
download = form.getvalue('download' ,False)
if download:
	download = cgi.escape(download)
committeeNameID = form.getvalue('committeeNameID' ,False)
if committeeNameID:
	committeeNameID = cgi.escape(committeeNameID)
entityOneType = form.getvalue('entityOneType' ,False)
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
transactionType = form.getvalue('transactionType' ,False)
if transactionType:
	transactionType = cgi.escape(transactionType)
startDate = form.getvalue('startDate' ,False)
if startDate:
	startDate = cgi.escape(startDate)
endDate = form.getvalue('endDate' ,False)
if endDate:
	endDate = cgi.escape(endDate)
report = cfquery.getreport(committeeNameID, entityOneType, entityOneFirstName, entityOneLastName, cycleName, transactionType, startDate, endDate, download)
#begin web content
print "content-type:text/html"
print
#print contents of report
if entityOneType <> "blank":
	if len(report) > 0:
		print json.dumps(report)
