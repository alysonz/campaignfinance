#!/usr/bin/python
#import resources
import cgi
import cgitb
import cfquery
def log(message):
	file = open("/var/log/apache2/alyson.log","a")
	file.write(message)
	file.write("\n")
	file.close()

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
endDate = form.getvalue('endDate' ,False)
if endDate:
	endDate = cgi.escape(endDate)
report = cfquery.getreport(committeeNameID, entityOneType, entityOneFirstName, entityOneLastName, cycleName, transactionType, startDate, endDate)
#begin web content
print "content-type:text/html"
print
print """
<html>
<body>
"""
#print contents of report
if entityOneType <> "blank":
	print "<p><a href='http://wildfire.codercollective.org/testcampaignfinance/download.cgi?entityOneType=%s&transactionType=%s&cycleName=%s&startDate=%s&endDate=%s&committeeNameID=%s&entityOneFirstName=%s&entityOneLastName=%s'>Download data</a></p>"%(entityOneType, transactionType, cycleName, startDate, endDate, committeeNameID, entityOneFirstName, entityOneLastName)
	print "<table border='1' width='3450'>"
	if len(report) > 0:
		for line in report:
			print "<tr>"
			for item in line:
				print "<td width='150'>%s</td>" % (item)
			print "</tr>"
	print "</table>"	

#unless they didn't select an entity type. Then inform the user.
else:
	print "Error 2: Please select a type for primary entity."
print """
</body>
</html>
"""
