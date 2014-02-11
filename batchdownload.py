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
db.commit()
cursor.close()
