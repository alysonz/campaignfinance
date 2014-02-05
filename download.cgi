#!/usr/bin/python
#import resources
import cgi
import cgitb
import cfquery
#get form variables
form = cgi.FieldStorage()
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
if startDate == "False":
	startDate = False
endDate = form.getvalue('endDate' ,False)
if endDate:
	endDate = cgi.escape(endDate)
if endDate == "False":
	endDate = False
report = cfquery.getreport(committeeNameID, entityOneType, entityOneFirstName, entityOneLastName, cycleName, transactionType, startDate, endDate)
#begin web content
download = "data.csv"
print "content-type:text/csv"
print "Content-disposition: attachment;filename=%s"%(download)
print
if entityOneType <> "blank":
	if len(report) > 0:
		for line in report:
			line = [str(x) for x in line]
			line = "|".join(line)
			line = line.rstrip()
			print line
#unless they didn't select an entity type. Then inform the user.
else:
	print "Error 2: Please select a type for primary entity."
