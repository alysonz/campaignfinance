#reformat and label names
from datetime import datetime
import calendar
import re
committees = open('committeesConsolidated.txt', 'r')
committeesFormat = open('committeesFormat.txt','w')
committees = committees.readlines()
organizationDate = 1
terminationDate = 1
cycleBeginDate = 1
cycleEndDate = 1
unixOrganizationDate = 1
unixTerminationDate = 1
unixCycleBeginDate = 1
unixCycleEndDate = 1
for line in committees:
#split committee data into columns
	items = line.split("|")
	#the 20th column is organization date
	organizationDate = items[19]
	#split date information MM/DD/YYYY HH:MM:SS at the space
	organizationDate = organizationDate.split(" ")
	#discard time data
	organizationDate = organizationDate[0]
	#split date
	organizationDate = organizationDate.split("/")
	#weed out null and atypical placeholder values (eg. 'N/A')
	if len(organizationDate) > 2:
		#create a datetime object. cast list values as integers and convert with datetime(YYYY, MM, DD, 0, 0)
		unixOrganizationDate = datetime(int(organizationDate[2]), int(organizationDate[0]), int(organizationDate[1]), 0, 0)
		#take datetime object and convert into unix timestamp
		unixOrganizationDate = calendar.timegm(unixOrganizationDate.utctimetuple())
		#replace old date with unix timestamp
		items[19] = str(unixOrganizationDate)
		#insert parsed year, month, day values as new fields
		items.insert(20, organizationDate[2])
		items.insert(21, organizationDate[0])
		items.insert(22, organizationDate[1])
	#select null and atypical placeholder values
	else:
		#normalize all to null
		items[19] = ""
		#insert empty fields for year, month, day values
		items.insert(20, "")
		items.insert(21, "")
		items.insert(22, "")
	#the now-24th item is termination date. repeat process.
	terminationDate	= items[23]
	terminationDate = terminationDate.split(" ")
	terminationDate = terminationDate[0]
	terminationDate = terminationDate.split("/")
	if len(terminationDate) > 2:
		unixTerminationDate = datetime(int(terminationDate[2]), int(terminationDate[0]), int(terminationDate[1]), 0, 0)
		unixTerminationDate = calendar.timegm(unixTerminationDate.utctimetuple())
		items[23] = str(unixTerminationDate)
		items.insert(24, terminationDate[2])
		items.insert(25, terminationDate[0])
		items.insert(26, terminationDate[1])
	else:
		items[23] = ""
		items.insert(24, "")
		items.insert(25, "")
		items.insert(26, "")
	#the now-37th item is cycle begin date. repeat process.
	cycleBeginDate = items[36]
	cycleBeginDate = cycleBeginDate.split(" ")
	cycleBeginDate = cycleBeginDate[0]
	cycleBeginDate = cycleBeginDate.split("/")
	if len(cycleBeginDate) > 2:
		unixCycleBeginDate = datetime(int(cycleBeginDate[2]), int(cycleBeginDate[0]), int(cycleBeginDate[1]), 0, 0)
		unixCycleBeginDate = calendar.timegm(unixCycleBeginDate.utctimetuple())
		items[36] = str(unixCycleBeginDate)
		items.insert(37, cycleBeginDate[2])
		items.insert(38, cycleBeginDate[0])
		items.insert(39, cycleBeginDate[1])
	else:
		items[36] = ""
		items.insert(37, "")
		items.insert(38, "")
		items.insert(39, "")
	#the now 41st item is cycle end date. repeat proces.
	cycleEndDate = items[40]
	cycleEndDate = cycleEndDate.split(" ")
	cycleEndDate = cycleEndDate[0]
	cycleEndDate = cycleEndDate.split("/")
	if len(cycleEndDate) > 2:
		unixCycleEndDate = datetime(int(cycleEndDate[2]), int(cycleEndDate[0]), int(cycleEndDate[1]), 0, 0)
		unixCycleEndDate = calendar.timegm(unixCycleEndDate.utctimetuple())
		items[40] = str(unixCycleEndDate)
		items.insert(41, cycleEndDate[2])
		items.insert(42, cycleEndDate[0])
		items.insert(43, cycleEndDate[1])
	else:
		items[40] = ""
		items.insert(41, "")
		items.insert(42, "")
		items.insert(43, "")
	line = "|".join(items)
	line = line.rstrip()	
	committeesFormat.write("%s\n" %(line))
