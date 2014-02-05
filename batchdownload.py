#!/usr/bin/python
#import resources
import MySQLdb
import re
from datetime import datetime
import calendar
from gettuple import gettuple
from gettuple import getlist
import os
import cgi
import cgitb
from parms import *
#connect to database
db = MySQLdb.connect(user=db_user, passwd=db_pass, db=db_db)
cursor = db.cursor()	
#individual query variables
committee = "you misspelled something somewhere"
committeeName = "you misspelled something somewhere"
report = []
cycleFilter = []
recipient = "you misspelled something somewhere"
transactions = "you misspelled something somewhere"
committeeTransaction = "you misspelled something somewhere"
headers = ['Committee Type','Committee Name', 'Committee Party', 'Committee Office', 'Incumbent: 1 = Yes', 'Transaction Type', 'Transaction Date', 'Transaction Amount', 'Transaction Memo', 'Transaction Category Name', 'Contributor/Payee Type', 'C/P First Name', 'C/P Last Name', 'C/P Address 1', 'C/P Address 2', 'C/P City', 'C/P State', 'C/P Zipcode', 'C/P Occupation', 'C/P Employer']
cursor.execute("select * from committees where officeName = 'State Treasurer' and cycleName = 2014;")
committee = cursor.fetchall()
cursor.execute("select unixCycleBeginDate, unixCycleEndDate from cycles where cycleName = 2014;")
cycleDates = gettuple(cursor.fetchall())
'''
if len(committee) > 1:
	committee = getlist(committee)
	for line in committee:
		report = []
		cursor.execute("select * from names where nameID = %s;",(line[1]))
		committeeName = gettuple(cursor.fetchall())
		cursor.execute("select * from transactions where committeeID = %s;",(line[0]))
		transactions = cursor.fetchall()
		if len(transactions) > 1:
			transactions = getlist(transactions)
			for item in transactions:
				cursor.execute("select * from names where nameID = %s;",(item[10]))
				recipient = gettuple(cursor.fetchall())
				committeeTransaction = committeeName[2:4] + line[31:33] + [line[34]] + [item[3]] + [item[5]] + [item[9]] + item[13:15] + [recipient[2]] + [recipient[4]] + [recipient[3]] + recipient[7:12] + recipient[13:15]
				report.append(committeeTransaction)
			cycleFilter = []
			for item in report:
				if (item[6] >= cycleDates[0]) and (item[6] <= cycleDates[1]):
					cycleFilter.append(item)
			report = cycleFilter
			if len(report) > 0:
				for item in report:
					item[6] = datetime.fromtimestamp(item[6]).strftime('%m-%d-%Y')
				report.insert(0, headers)
			reportWrite = open('/var/www/campaignfinance/batch/%s.txt'%(committeeName[3]),'w')
			if len(report) > 0:
				for item in report:
					item = [str(x) for x in item]
					item = "|".join(item)
					item = item.rstrip()
					reportWrite.write("%s\n" % (item))
			else:
				reportWrite.write("No transactions have been reported yet for this committee for 2014.")
		elif len(transactions) == 1:
			transactions = gettuple(transactions)
			cursor.execute("select * from names where nameID = %s;",(transactions[10]))
			recipient = gettuple(cursor.fetchall())
			committeeTransaction = committeeName[2:4] + line[31:33] + [line[34]] + [transactions[3]] + [transactions[5]] + [transactions[9]] + transactions[13:15] + [recipient[2]] + [recipient[4]] + [recipient[3]] + recipient[7:12] + recipient[13:15]
			report.append(committeeTransaction)
			for item in report:
				if (item[6] >= cycleDates[0]) and (item[6] <= cycleDates[1]):
					print "yay"
				else:
					report = []
			if len(report) > 0:	
				for item in report:
					item[6] = datetime.fromtimestamp(item[6]).strftime('%m-%d-%Y')
				report.insert(0,headers)
			reportWrite = open('/var/www/campaignfinance/batch/%s.txt'%(committeeName[3]),'w')
			if len(report) > 0:
				for item in report:
					item = [str(x) for x in item]
					item = "|".join(item)
					item = item.rstrip()
					reportWrite.write("%s\n" % (item))
			else:
				reportWrite.write("No transactions have been reported yet for this committee for 2014.")
		elif len(transactions) == 0:
			reportWrite = open('/var/www/campaignfinance/batch/%s.txt'%(committeeName[3]),'w')
			reportWrite.write("No transactions have been reported yet for this committee for 2014.")
		report = []
elif len(committee) == 1:
	committee = gettuple(committee)
	cursor.execute("select * from names where nameID = %s;",(committee[1]))
	committeeName = gettuple(cursor.fetchall())
	cursor.execute("select * from transactions where committeeID = %s;",(committee[0]))
	transactions = cursor.fetchall()
	if len(transactions) > 1:
		transactions = getlist(transactions)
		for item in transactions:
			cursor.execute("select * from names where nameID = %s;",(item[10]))
			recipient = gettuple(cursor.fetchall())
			committeeTransaction = committeeName[2:4] + committee[31:33] + [committee[34]] + [item[3]] + [item[5]] + [item[9]] + item[13:15] + [recipient[2]] + [recipient[4]] + [recipient[3]] + recipient[7:12] + recipient[13:15]
			report.append(committeeTransaction)
		for item in report:
			if (item[6] >= cycleDates[0]) and (item[6] <= cycleDates[1]):
				cycleFilter.append(item)
		report =  cycleFilter
		if len(report) > 0:
			for item in report:
				item[6] = datetime.fromtimestamp(item[6]).strftime('%m-%d-%Y')
			report.insert(0, headers)
		reportWrite = open('/var/www/campaignfinance/batch/%s.txt'%(committeeName[3]),'w')
		if len(report) > 0:
			for line in report:
				line = [str(x) for x in line]
				line = "|".join(line)
				line = line.rstrip()
				reportWrite.write("%s\n" % (line))
	if len(transactions) == 1:
		transactions = gettuple(transactions)
		cursor.execute("select * from names where nameID = %s;",(transactions[10]))
		recipient = gettuple(cursor.fetchall())
		committeeTransaction = committeeName[2:4] + committee[31:33] + [committee[34]] + [transactions[3]] + [transactions[5]] + [transactions[9]] + transactions[13:15] + [recipient[2]] + [recipient[4]] + [recipient[3]] + recipient[7:12] + recipient[13:15]
		report.append(committeeTransaction)
		if (report[6] >= cycleDates[0]) and (report[6] <= cycleDates[1]):
			print "yay"
		else:
			report = []
		if len(report) > 0:
			report[6] = datetime.fromtimestamp(report[6]).strftime('%m-%d-%Y')
			report.insert(0, headers)
		reportWrite = open('/var/www/campaignfinance/batch/%s.txt'%(committeeName[3]),'w')
		if len(report) > 0:
			for item in report:
				item = [str(x) for x in item]
				item = "|".join(item)
				item = item.rstrip()
				reportWrite.write("%s\n" % (item))
		else:
			reportWrite.write("No transactions have been reported yet for this committee for 2014.")
	if len(transactions) == 0:
		reportWrite = open('/var/www/campaignfinance/batch/%s.txt'%(committeeName[3]),'w')
		reportWrite.write("No transactions have been reported yet for this committee for 2014.")
'''







'''
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
				for line in report:
					line[6] = datetime.fromtimestamp(line[6]).strftime('%m-%d-%Y')
			report.insert(0,headers)
		#if for some reason they entered the committee id incorrectly and nothing was returned, inform the user
		#BUT IT DOESNT WORK FOR SOME REASON
		else:
			errorReport.append("Message 12: incorrect committee ID")
'''
db.commit()
cursor.close()
