#!/usr/bin/python
#import resources
import MySQLdb
import re
from datetime import datetime
import calendar
from gettuple import gettuple
from gettuple import getlist
import os
from parms import *
def getreport(committeeNameID, entityOneType, entityOneFirstName, entityOneLastName, cycleName, transactionType, startDate, endDate):
	#connect to database
	db = MySQLdb.connect(user=db_user, passwd=db_pass, db=db_db)
	cursor = db.cursor()	
	#individual query variables
	committee = "you misspelled something somewhere"
	individualNames = "you misspelled something somewhere"
	candidateName = "you misspelled something somewhere"
	committeeName = "you misspelled something somewhere"
	individualTransaction = "you misspelled something somewhere"
	reportName = []
	individualLine = 0
	report = []
	cycleDates = "you misspelled something somewhere"
	individualFilter = []
	transactionDate = "you misspelled something somewhere"
	headers = "you misspelled something somewhere"
	startDateTmp = "you misspelled something somewhere"
	endDateTmp = "you misspelled something somewhere"
	recipient = "you misspelled something somewhere"
	transactions = "you misspelled something somewhere"
	errorReport = []
	transactionsCycleFilter = []
	transactionsTypeFilter = []
	transactionFilter = []
	hold = []
	#begin individual query
	if (entityOneType == "individual") and (entityOneFirstName or entityOneLastName):
		#set up column names for report
		headers = ['Contributor/Payee Type', 'C/P First Name', 'C/P Last Name', 'C/P Middle Name', 'C/P Suffix','C/P Address 1', 'C/P Address 2', 'C/P City', 'C/P State', 'C/P Zipcode', 'C/P Occupation', 'C/P Employer', 'Committee Name', 'Candidate First Name', 'Candidate Last Name', 'Committee Party', 'Committee Office', 'Incumbent: 1 = Yes', 'Transaction Type', 'Transaction Date', 'Transaction Amount', 'Transaction Memo', 'Transaction Category Name']
		#search names for partial first and last name from form
		cursor.execute("select * from names where (entityTypeName = 'Business' or entityTypeName = 'Individual') and lastName like %s and firstName like %s;",("%%%s%%"%(entityOneLastName),"%%%s%%"%(entityOneFirstName)))
		#fetch results
		individualNames = cursor.fetchall()
		#in the most likely event that there is more than one individual, or more than one instance of one individual associated with the partial name...
		if len(individualNames) > 1:
			#make individualNames a list of lists
			individualNames = getlist(individualNames)
			#for each name result
			for line in individualNames:
				#select all corresponding transactions relating to the name result
				cursor.execute("select * from transactions where nameID = %s;",(line[0]))
				individualTransaction = cursor.fetchall()
				#if there is more than one transaction relating to this nameID
				if len(individualTransaction) > 1:
					#make individualTransactions a list of lists	
					individualTransaction = getlist(individualTransaction)
					#for each transaction
					for instance in individualTransaction:
						#select the committee information associated with the reported transaction. There will only ever be one.
						cursor.execute("select * from committees where committeeID = %s;",(instance[4]))
						#make that information into a list
						committee = gettuple(cursor.fetchall())
						#if the committee is a candidate committee and has a candidate ID, retrieve the candidate's information
						if committee[4] <> 0:
							cursor.execute("select * from names where nameID = %s;",(committee[4]))
							#turn the information into a list
							candidateName = gettuple(cursor.fetchall())
							#and discard everything that isn't the last and first name
							candidateName = candidateName[3:5]
						#If the committee does not have an associated candidate, create placeholders
						else:
							candidateName = [0,0]
						#select the name information for the committee associated with the transaction
						cursor.execute("select * from names where nameID = %s;",(committee[1]))
						#turn that information into a list
						committeeName = gettuple(cursor.fetchall())
						#create a list that contains only the information corresponding to column headers in report
						individualLine = [line[2]] + [line[4]] + [line[3]] + line[5:12] + line[13:15] + [committeeName[3]] + [candidateName[1]] + [candidateName[0]] + committee[31:33] + [committee[34]] + [instance[3]] + [instance[5]] + [instance[9]] + instance[13:15]
						#append this line to report
						report.append(individualLine)
				#if there is only one transaction associated with each individual
				if len(individualTransaction) == 1:
					#turn the transaction information into a list
					individualTransaction = gettuple(individualTransaction)
					#select the committee information associated with the reported transaction. There will only ever be one.
					cursor.execute("select * from committees where committeeID = %s;",(individualTransaction[4]))
					#make that information into a list
					committee = gettuple(cursor.fetchall())
					#if the committee is a candidate committee and has a candidate ID, retrieve the candidate's information
					if committee[4] <> 0:
						cursor.execute("select * from names where nameID = %s;",(committee[4]))
						#turn the information into a list
						candidateName = gettuple(cursor.fetchall())
						#and discard everything that isn't the last and first name
						candidateName = candidateName[3:5]
					#If the committee does not have an associated candidate, create placeholders
					else:
						candidateName = [0,0]
					#select the name information for the committee associated with the transaction
					cursor.execute("select * from names where nameID = %s;",(committee[1]))
					#turn that information into a list
					committeeName = gettuple(cursor.fetchall())
					#create a list that contains only the information corresponding to column headers in report
					individualLine = [line[2]] + [line[4]] + [line[3]] + line[5:12] + line[13:15] + [committeeName[3]] + [candidateName[1]] + [candidateName[0]] + committee[31:33] + [committee[34]] + [individualTransaction[3]] + [individualTransaction[5]] + [individualTransaction[9]] + individualTransaction[13:15]
					#append this line to report
					report.append(individualLine)
				#If for some reason there are no associated transactions which is tech. possible, inform the user
				if len(report) == 0:
					errorReport.append("Message 1: No transactions found.")
		#in the event that there is only one individual that matches the partial first and last name
		elif len(individualNames) == 1:
			#turn that result into a list
			individualNames = gettuple(individualNames)
			#select the transactions associated with that individual
			cursor.execute("select * from transactions where nameID = %s;",(individualNames[0]))
			individualTransaction = cursor.fetchall()
			#if there is more than one transaction associated with that individual, follow the corresponding proceedures as detailed above
			if len(individualTransaction) > 1:
				individualTransaction = getlist(individualTransaction)
				for instance in individualTransaction:
					cursor.execute("select * from committees where committeeID = %s;",(instance[4]))
					committee = gettuple(cursor.fetchall())
					if committee[4] <> 0:
						cursor.execute("select * from names where nameID = %s;",(committee[4]))
						candidateName = gettuple(cursor.fetchall())
						candidateName = candidateName[3:5]
					else:
						candidateName = [0,0]
					cursor.execute("select * from names where nameID = %s;",(committee[1]))
					committeeName = gettuple(cursor.fetchall())
					individualLine = [individualNames[2]] + [individualNames[4]] + [individualNames[3]] + individualNames[5:12] + individualNames[13:15] + [committeeName[3]] + [candidateName[1]] + [candidateName[0]] + committee[31:33] + [committee[34]] + [instance[3]] + [instance[5]] + [instance[9]] + instance[13:15]
					report.append(individualLine)
			#if there is only one transaction associated with that individual, follow the corresponding proceedures as detailed above
			if len(individualTransaction) == 1:
				individualTransaction = gettuple(individualTransaction)
				cursor.execute("select * from committees where committeeID = %s;",(individualTransaction[4]))
				committee = gettuple(cursor.fetchall())
				if committee[4] <> 0:
					cursor.execute("select * from names where nameID = %s;",(committee[4]))
					candidateName = gettuple(cursor.fetchall())
					candidateName = candidateName[3:5]
				else:
					candidateName = [0,0]
				cursor.execute("select * from names where nameID = %s;",(committee[1]))
				committeeName = gettuple(cursor.fetchall())
				individualLine = [individualNames[2]] + [individualNames[4]] + [individualNames[3]] + individualNames[5:12] + individualNames[13:15] + [committeeName[3]] + [candidateName[1]] + [candidateName[0]] + committee[31:33] + [committee[34]] + [individualTransaction[3]] + [individualTransaction[5]] + [individualTransaction[9]] + individualTransaction[13:15]
				report.append(individualLine)
			#if for some reason the name has no related transactions which is technically possible I guess, inform the user
			if len(report) == 0:
				errorReport.append("Message 2: No transactions found.")
		#If there is no individual that matches the partial first and last name, inform the user
		elif len(individualNames) == 0:
			errorReport.append("Message 3: Individual not found.")
		#time filter:
		if cycleName:
			if len(report) > 0:
				individualFilter = []
				if cycleName <> "all":
					cursor.execute("select unixCycleBeginDate, unixCycleEndDate from cycles where cycleName = %s;",(cycleName))
					cycleDates = gettuple(cursor.fetchall())	
					for line in report:
						if (line[19] >= cycleDates[0]) and (line[19] <= cycleDates[1]):
							individualFilter.append(line)
					report = individualFilter
		if startDate:
			if len(report) > 0:
				individualFilter = []
				startDateTmp = startDate.split("/")
				if (len(startDateTmp[0]) == 2) and (len(startDateTmp[1]) == 2) and (len(startDateTmp[2]) == 4):
					startDateTmp = datetime(int(startDateTmp[2]),int(startDateTmp[0]),int(startDateTmp[1]),0,0)
					startDateTmp = calendar.timegm(startDateTmp.utctimetuple())
					for line in report:
						if line[19] >= startDateTmp:
							individualFilter.append(line)
					report = individualFilter
				else:
					errorReport.append("Message 10: Invalid date format.")
		if endDate:
			if len(report) > 0:
				individualFilter = []
				endDateTmp = endDate.split("/")
				if (len(endDateTmp[0]) == 2) and (len(endDateTmp[1]) == 2) and (len(endDateTmp[2]) == 4):
					endDateTmp = datetime(int(endDateTmp[2]),int(endDateTmp[0]),int(endDateTmp[1]),0,0)
					endDateTmp = calendar.timegm(endDateTmp.utctimetuple())
					for line in report:
						if line[19] <= endDateTmp:
							individualFilter.append(line)
					report = individualFilter
				else:
					errorReport.append("Message 11: Invalid date format.")
		if transactionType == "income":
			if len(report) > 0:
				individualFilter = []
				for line in report:
					if line[18] == "Income":
						individualFilter.append(line)
				report = individualFilter		
		if transactionType == "expense":
			if len(report) > 0:
				individualFilter = []
				for line in report:
					if line[18] == "Expense":
						individualFilter.append(line)
				report = individualFilter
				if len(report) == 0:
					errorReport.append("Message 16: No expenses were paid to %s %s."%(entityOneFirstName, entityOneLastName))
		if len(report) > 0:
			for line in report:
				line[19] = datetime.fromtimestamp(line[19]).strftime('%m-%d-%Y')
		report.insert(0, headers)
		report.insert(0, [entityOneFirstName, entityOneLastName])
	elif entityOneType <> "committee":
		report.append(["Message 18: Please fill in at least a partial first name or partial last name for individual searches."])
	#End individual query 
	if entityOneType == "committee":
		#select name information for the nameID from the form
		cursor.execute("select * from names where nameID = %s;",(committeeNameID))
		#turn that information into a list
		committeeName = gettuple(cursor.fetchall())
		#make sure the committee exists (no errors in inputting the id)
		if len(committeeName) > 0:
			#select the committee information
			cursor.execute("select * from committees where nameID = %s;",(committeeName[0]))
			#turn information into a list
			committee = gettuple(cursor.fetchall())
			#select transactions associated with the commmittee
			cursor.execute("select * from transactions where committeeID = %s;",(committee[0]))
			#turn information into a list of lists
			transactions = getlist(cursor.fetchall())
			#set up report column headings
			headers = ['Committee Type','Committee Name', 'Committee Party', 'Committee Office', 'Incumbent: 1 = Yes', 'Transaction Type', 'Transaction Date', 'Transaction Amount', 'Transaction Memo', 'Transaction Category Name', 'Contributor/Payee Type', 'C/P First Name', 'C/P Last Name', 'C/P Address 1', 'C/P Address 2', 'C/P City', 'C/P State', 'C/P Zipcode', 'C/P Occupation', 'C/P Employer']
			for line in transactions:
				#select information about the contributor or payee involved in each transaction
				cursor.execute("select * from names where nameID = %s;",(line[10]))	
				recipient = gettuple(cursor.fetchall())		
				#build list that contains only the information referenced in the report headings
				committeeTransaction = committeeName[2:4] + committee[31:33] + [committee[34]] + [line[3]] + [line[5]] + [line[9]] + line[13:15] + [recipient[2]] + [recipient[4]] + [recipient[3]] + recipient[7:12] + recipient[13:15]
				#append that new line to reports
				report.append(committeeTransaction)
			if cycleName:
				if len(report) > 0:
					individualFilter = []
					if cycleName <> "all":
						cursor.execute("select unixCycleBeginDate, unixCycleEndDate from cycles where cycleName = %s;",(cycleName))
						cycleDates = gettuple(cursor.fetchall())
						for line in report:
							if (line[6] >= cycleDates[0]) and (line[6] <= cycleDates[1]):
								individualFilter.append(line)
						report = individualFilter
						if len(report) == 0:
							errorReport.append("Message 13: No transactions exist for this committee in the %s cycle"%cycleName)
			if startDate:
				if len(report) > 0:
					individualFilter = []
					startDateTmp = startDate.split("/")
					if (len(startDateTmp[0]) == 2) and (len(startDateTmp[1]) == 2) and (len(startDateTmp[2]) == 4):
						startDateTmp = datetime(int(startDateTmp[2]),int(startDateTmp[0]),int(startDateTmp[1]),0,0)
						startDateTmp = calendar.timegm(startDateTmp.utctimetuple())
						for line in report:
							if line[6] >= startDateTmp:
								individualFilter.append(line)
						report = individualFilter
						if len(report) == 0:
							errorReport.append("Message 14: No transactions exist for this committee on or after %s"%startDate)
					else:
						errorReport.append("Message 10: Invalid date format.")
			if endDate:
				if len(report) > 0:
					individualFilter = []
					endDateTmp = endDate.split("/")
					if (len(endDateTmp[0]) == 2) and (len(endDateTmp[1]) == 2) and (len(endDateTmp[2]) == 4):
						endDateTmp = datetime(int(endDateTmp[2]),int(endDateTmp[0]),int(endDateTmp[1]),0,0)
						endDateTmp = calendar.timegm(endDateTmp.utctimetuple())
						for line in report:
							if line[6] <= endDateTmp:
								individualFilter.append(line)
						report = individualFilter
						if len(report) == 0:
							errorReport.append("Message 15: No transactions exist for this committee on or before %s"%endDate)
					else:
						errorReport.append("Message 11: Invalid date format.")
			if transactionType:
				if len(report) > 0:
					individualFilter = []
					if transactionType == "expense":
						for line in report:
							if line[5] == "Expense":
								individualFilter.append(line)
						report = individualFilter
						if len(report) == 0:
							errorReport.append("Message 17: No such expenses exist for this committee.")
					if transactionType == "income":
						for line in report:
							if line[5] == "Income":
								individualFilter.append(line)
						report = individualFilter
						if len(report) == 0:
							errorReport.append("Message 17: No such income exist for this committee.")
			if len(report) > 0:
				if len(report) > 1:
					for line in report:
						line[6] = datetime.fromtimestamp(line[6]).strftime('%m-%d-%Y')
				else:
					for line in report:
						line[6] = datetime.fromtimestamp(line[6]).strftime('%m-%d-%Y')
			report.insert(0,headers)
			report.insert(0,[committeeNameID])
		#if for some reason they entered the committee id incorrectly and nothing was returned, inform the user
		#BUT IT DOESNT WORK FOR SOME REASON
		else:
			errorReport.append("Message 12: incorrect committee ID")
	db.commit()
	cursor.close()
	if len(errorReport) > 0:
		report.insert(1,errorReport)
		report.insert(1,startDate)
		report.insert(1,endDate)
	return report


