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
searchType = form.getvalue('searchType', False)
if searchType:
	searchType = cgi.escape(searchType)
race = form.getvalue('race', False)
if race:
	race = cgi.escape(race)
cycleName = form.getvalue('cycleName', False)
if cycleName:
	cycleName = cgi.escape(cycleName)
firstName = form.getvalue('firstName', '')
if firstName:
	firstName = cgi.escape(firstName)
lastName = form.getvalue('lastName', '')
if lastName:
	lastName = cgi.escape(lastName)
committee = form.getvalue('committee', False)
if committee:
	committee = cgi.escape(committee)

#get report
report = 0
if searchType == 'race':
	report = queryByRace(unicode(race), cycleName)
elif searchType == 'candidate':
	report = queryByCandidate(firstName, lastName)
elif searchType == 'committee':
	report = queryByCommittee(committee)


#begin web content
print 'Content-Type: application/json\n\n'
print
#print contents of report
if report:
	print json.dumps(report)
else:
	report = 'No results found'
	print json.dumps(report)
