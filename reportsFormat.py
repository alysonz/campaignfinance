#reformat and label names
from datetime import datetime
import calendar
import re
reports = open('reportsConsolidated.txt', 'r')
reportsFormat = open('reportsFormat.txt','w')
reports = reports.readlines()
reportPeriodBeginDate = 1
reportPeriodEndDate = 1
filingPeriodBeginDate = 1
filingPeriodEndDate = 1
filingDate = 1
cycleName = 1
unixReportPeriodBeginDate = 1
unixReportPeriodEndDate = 1
unixFilingPeriodBeginDate = 1
unixFilingPeriodEndDate = 1
unixFilingDate = 1
for line in reports:
#split committee data into columns
	items = line.split("|")
	#the 6th column is report period begin date
	reportPeriodBeginDate = items[5]
	#split date information MM/DD/YYYY HH:MM:SS at the space
	reportPeriodBeginDate = reportPeriodBeginDate.split(" ")
	#discard time data
	reportPeriodBeginDate = reportPeriodBeginDate[0]
	#split date
	reportPeriodBeginDate = reportPeriodBeginDate.split("/")
	#weed out null and atypical placeholder values (eg. 'N/A')
	if len(reportPeriodBeginDate) > 2:
		#create a datetime object. cast list values as integers and convert with datetime(YYYY, MM, DD, 0, 0)
		unixReportPeriodBeginDate = datetime(int(reportPeriodBeginDate[2]), int(reportPeriodBeginDate[0]), int(reportPeriodBeginDate[1]), 0, 0)
		#take datetime object and convert into unix timestamp
		unixReportPeriodBeginDate = calendar.timegm(unixReportPeriodBeginDate.utctimetuple())
		#replace old date with unix timestamp
		items[5] = str(unixReportPeriodBeginDate)
		#insert parsed year, month, day values as new fields
		items.insert(6, reportPeriodBeginDate[2])
		items.insert(7, reportPeriodBeginDate[0])
		items.insert(8, reportPeriodBeginDate[1])
	#select null and atypical placeholder values
	else:
		#normalize all to null
		items[5] = "0"
		#insert empty fields for year, month, day values
		items.insert(6, "0")
		items.insert(7, "0")
		items.insert(8, "0")
	#the 10th item is report period end date. repeat process.
	reportPeriodEndDate	= items[9]
	reportPeriodEndDate = reportPeriodEndDate.split(" ")
	reportPeriodEndDate = reportPeriodEndDate[0]
	reportPeriodEndDate = reportPeriodEndDate.split("/")
	if len(reportPeriodEndDate) > 2:
		unixReportPeriodEndDate = datetime(int(reportPeriodEndDate[2]), int(reportPeriodEndDate[0]), int(reportPeriodEndDate[1]), 0, 0)
		unixReportPeriodEndDate = calendar.timegm(unixReportPeriodEndDate.utctimetuple())
		items[9] = str(unixReportPeriodEndDate)
		items.insert(10, reportPeriodEndDate[2])
		items.insert(11, reportPeriodEndDate[0])
		items.insert(12, reportPeriodEndDate[1])
	else:
		items[9] = "0"
		items.insert(10, "0")
		items.insert(11, "0")
		items.insert(12, "0")
	#the 14th item is filing period begin date. repeat process.
	filingPeriodBeginDate = items[13]
	filingPeriodBeginDate = filingPeriodBeginDate.split(" ")
	filingPeriodBeginDate = filingPeriodBeginDate[0]
	filingPeriodBeginDate = filingPeriodBeginDate.split("/")
	if len(filingPeriodBeginDate) > 2:
		unixFilingPeriodBeginDate = datetime(int(filingPeriodBeginDate[2]), int(filingPeriodBeginDate[0]), int(filingPeriodBeginDate[1]), 0, 0)
		unixFilingPeriodBeginDate = calendar.timegm(unixFilingPeriodBeginDate.utctimetuple())
		items[13] = str(unixFilingPeriodBeginDate)
		items.insert(14, filingPeriodBeginDate[2])
		items.insert(15, filingPeriodBeginDate[0])
		items.insert(16, filingPeriodBeginDate[1])
	else:
		items[13] = "0"
		items.insert(14, "0")
		items.insert(15, "0")
		items.insert(16, "0")
	#the 18th item is filing period end date. repeat proces.
	filingPeriodEndDate = items[17]
	filingPeriodEndDate = filingPeriodEndDate.split(" ")
	filingPeriodEndDate = filingPeriodEndDate[0]
	filingPeriodEndDate = filingPeriodEndDate.split("/")
	if len(filingPeriodEndDate) > 2:
		unixFilingPeriodEndDate = datetime(int(filingPeriodEndDate[2]), int(filingPeriodEndDate[0]), int(filingPeriodEndDate[1]), 0, 0)
		unixFilingPeriodEndDate = calendar.timegm(unixFilingPeriodEndDate.utctimetuple())
		items[17] = str(unixFilingPeriodEndDate)
		items.insert(18, filingPeriodEndDate[2])
		items.insert(19, filingPeriodEndDate[0])
		items.insert(20, filingPeriodEndDate[1])
	else:
		items[17] = "0"
		items.insert(18, "0")
		items.insert(19, "0")
		items.insert(20, "0")
	#the 23nd item is filing date. repeat process.
	filingDate = items[22]
	filingDate = filingDate.split(" ")
	filingDate = filingDate[0]
	filingDate = filingDate.split("/")
	if len(filingDate) > 2:
		unixFilingDate = datetime(int(filingDate[2]), int(filingDate[0]), int(filingDate[1]), 0, 0)
		unixFilingDate = calendar.timegm(unixFilingDate.utctimetuple())
		items[22] = str(unixFilingDate)
		items.insert(23, filingDate[2])
		items.insert(24, filingDate[0])
		items.insert(25, filingDate[1])
	else:
		items[22] = "0"
		items.insert(23, "0")
		items.insert(24, "0")
		items.insert(25, "0")
	#convert cycleID to actual cycle year
	cycleName = int(items[2])
	if cycleName == 1:
		cycleName = 1994
	elif cycleName == 2:
		cycleName = 1996
	elif cycleName == 3:
		cycleName = 1998
	elif cycleName == 4:
		cycleName = 2000
	elif cycleName == 5:
		cycleName = 2002
	elif cycleName == 6:
		cycleName = 2004
	elif cycleName == 7:
		cycleName = 2006
	elif cycleName == 8:
		cycleName = 2008
	elif cycleName == 25:
		cycleName = 2010
	elif cycleName == 26:
		cycleName = 2012
	elif cycleName == 27:
		cycleName = 2014
	items[2] = str(cycleName)
	#normalize originalReportID
	if len(items[21]) < 1:
		items[21] = "0"
	line = "|".join(items)
	line = line.rstrip()	
	reportsFormat.write("%s\n" %(line))
