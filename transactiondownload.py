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
'''cursor.execute("select unixCycleBeginDate, unixCycleEndDate from cycles where cycleName = 2014;")
cycleDates = gettuple(cursor.fetchall())'''
cursor.execute("select * from transactions where (unixTransactionDate >= 1353974400 and unixTransactionDate <= 1416960000);")
transactions = getlist(cursor.fetchall())
for line in transactions:
	cursor.execute("select * from names where nameID = %s;",(line[10]))
	recipient = gettuple(cursor.fetchall())
	cursor.execute("select * from committees where committeeID = %s;",(line[4]))
	committee = gettuple(cursor.fetchall())
	cursor.execute("select * from names where nameID = %s;",(committee[1]))
	committeeName = gettuple(cursor.fetchall())
	committeeTransaction = committeeName[2:4] + committee[31:33] + [committee[34]] + [line[3]] +[line[5]] + [line[9]] + line[13:15] + [recipient[2]] + [recipient[4]] + [recipient[3]] + recipient[7:12] + recipient[13:15]
	committeeTransaction[6] = datetime.fromtimestamp(committeeTransaction[6]).strftime('%m-%d-%Y')
	report.append(committeeTransaction)
report.insert(0,headers)
reportWrite = open('/var/www/testcampaignfinance/2014transactions.txt','w')
for item in report:
	item = [str(x) for x in item]
	item = "|".join(item)
	item = item.rstrip()
	reportWrite.write("%s\n" % (item))
db.commit()
cursor.close()

