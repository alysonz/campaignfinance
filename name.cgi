#!/usr/bin/python
#import resources
import cgi
import cgitb
import MySQLdb
import re
from gettuple import getlist
from gettuple import gettuple
from parms import *
import json
#connect to database
db = MySQLdb.connect(user=db_user, passwd=db_pass, db=db_db)
cursor = db.cursor()
#get form variables
form = cgi.FieldStorage()
searchType = form.getvalue('searchType' ,False)
if searchType:
	searchType = cgi.escape(searchType)
firstName = form.getvalue('firstName', False)
if firstName:
	firstName= cgi.escape(firstName)
lastName = form.getvalue('lastName', False)
if lastName:
	lastName = cgi.escape(lastName)
race = form.getvalue('race' ,False)
if race:
	race = cgi.escape(race)
cycleName = form.getvalue('cycleName' ,False)
if cycleName:
	cycleName = cgi.escape(cycleName)
committeeForm = form.getvalue('committee', False)
if committeeForm:
	committeeForm = cgi.escape(committeeForm)
#committee query variables
nameResult = "you misspelled something somewhere"
committee = "you misspelled something somewhere"
committeeName = "you misspelled something somewhere"
monkey = "you misspelled something somewhere"
cycleDates = "you misspelled something somewhere"
possibleName = "you misspelled something somewhere"
report = []
committeesByRace = "you misspelled something somewhere"
#committee by race
if searchType == "race":
	if race <> "blank":
		if cycleName <> "blank":
			cursor.execute("select * from committees where officeName = %s and cycleName = %s;",(race, cycleName))
			committeesByRace = cursor.fetchall()
			if len(committeesByRace) > 1:
				committeesByRace = getlist(committeesByRace)
				for line in committeesByRace:
					cursor.execute("select nameID, lastName, firstName, entityTypeName from names where nameID = %s;",(line[1]))
					committeeName = gettuple(cursor.fetchall())
					committeeName.append(line[35])
					report.append(committeeName)	
			elif len(committeesByRace) == 1:
				committeesByRace = gettuple(committeesByRace)
				cursor.execute("select nameID, lastName, firstName, entityTypeName from names where nameID = %s;",(committeesByRace[1]))
				committeeName = gettuple(cursor.fetchall())
				committeeName.append(committeesByRace[35])
				report.append(committeeName)
			else:
				report = [["Message 12: No committees found."]]
		else:
			report = [["Message 11: Please select cycle."]]
	else:
		report = [["Message 14: Please select a race."]]
#committee query
if searchType == "committee":
	if committeeForm:
		cursor.execute("select nameID from names where lastName like %s;",("%%%s%%"%(committeeForm)))
		nameResult = gettuple(cursor.fetchall())
		if len(nameResult) > 0:
			for line in nameResult:
				cursor.execute("select committeeID from committees where nameID = %s;",(line))
				committee = gettuple(cursor.fetchall())
				if len(committee) > 0:
					cursor.execute("select nameID from committees where committeeID = %s;",(committee[0]))
					nameID = gettuple(cursor.fetchall())
					cursor.execute("select nameID, lastName, firstName, entityTypeName from names where nameID = %s;",(nameID[0]))
					possibleName = gettuple(cursor.fetchall())
					cursor.execute("select cycleName from committees where nameID = %s;",(nameID[0]))
					cycleName = gettuple(cursor.fetchall())
					possibleName.append(cycleName[0])
					#list of committee names		
					report.append(possibleName)
			if len(report) == 0:
				report = [["Message 4: Committee not found."]]		
		else:
			report = [["Message 5: Committee not found."]]
	else:
		report = [["Message 15: Minimum requirement not met. Please supply a full or partial committee name in last name field."]]
#end committee query
#begin candidate query
if searchType == "candidate":
	if (firstName) or (lastName):
		if firstName == False:
			firstName = ""
		if lastName == False:
			lastName = ""
		cursor.execute("select nameID from names where lastName like %s and firstName like %s;",("%%%s%%"%(lastName),"%%%s%%"%(firstName)))
		nameResult = gettuple(cursor.fetchall())
		if len(nameResult) > 1:
			for line in nameResult:
				cursor.execute("select * from committees where candidateNameID = %s;",(line))
				candidate = gettuple(cursor.fetchall())
				if len(candidate) > 0:
					#select the english name and nameID for the candidateID
					cursor.execute("select lastName, firstName from names where nameID = %s;",(candidate[4]))
					#make a list of that information
					possibleName = gettuple(cursor.fetchall())
					#append the cycle name from their committee information to their english name information
					possibleName.append(candidate[35])
					cursor.execute("select * from names where nameID = %s;",(candidate[1]))
					committeeName = gettuple(cursor.fetchall())
					possibleName.append(committeeName[3])
					possibleName.insert(0, candidate[1])
					#append each candidate's name to the final report
					report.append(possibleName)
					#if only one of the possible names is a candidate
				#if none of the names was a candidate, inform the user
			if len(report) == 0:
				report = [["Message 6: Candidate not found."]]
		#if there was only one name returned based on the partial first and last name from the form
		elif len(nameResult) == 1:
			#check against the committees table to see if that name is a candidate
			cursor.execute("select * from committees where candidateNameID = %s;",(nameResult[0]))
			#make a list of the committee information
			candidate = gettuple(cursor.fetchall())
			#if the name was a candidate and has corresponding committee information
			if len(candidate) > 0:
				#select the english name information for that candidate
				cursor.execute("select lastName, firstName from names where nameID = %s;",(candidate[4]))
				#turn that information into a list
				possibleName = gettuple(cursor.fetchall())
				#add the committee's cycle information to that list
				possibleName.append(candidate[35])
				possibleName.append(candidate[3])
				possibleName.append(candidate[1])
				#append that candidate's information to the final report
				report.append(possibleName)
			#if the name was not a candidate, inform the user
			else:
				report = [["Message 7: Candidate not found."]]
		#if there were no names returned based on the partial first and last name, inform the user
		else:
			report = [["Message 8: Candidate not found."]]		
	else:
		report = [["Message 14: Minimum requirements not met. Please supply at least a partial first or last name."]]
db.commit()
cursor.close()
#begin web content
print "content-type:text/html"
print
print """
<html>
<body>
"""
if len(report) > 0:
	print json.dumps(report)
print """
</body>
</html>
"""
