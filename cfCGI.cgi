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

#get form variables
form = cgi.FieldStorage()

download = form.getvalue('download' ,False)
if download:
	download = cgi.escape(download)

committeeID = form.getlist('committeeID')

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

#get report
if committeeID:
	report = committeeQuery(committeeID)
else:
	report = individualQuery(entityOneLastName, entityOneFirstName)
"""
#filter
if cycleName != "All":
	report = cycle(cycleName, report)
if transactionType != "All":
	report = incomeExpense(transactionType, report)
if startDate:
	report = date(startDate, "begin", report)
if endDate:
	report = date(endDate, "end", report)

#finalize
report = convertDate(report)
"""


#begin web content
print 'Content-Type: application/json\n\n'
print
#print contents of report
print json.dumps(committeeID);
if entityOneType == "blank":
	if len(report) > 0:
		print json.dumps(report)
