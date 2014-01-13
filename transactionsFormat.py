#reformat and label names
from datetime import datetime
import calendar
import re
transactions = open('transactionsConsolidated.txt', 'r')
transactionsFormat = open('transactionsFormat.txt','w')
transactionDate = 1
unixTransactionDate = 1
transactionAmount = 1
line = transactions.readline()
index = 0
while line:
	index+=1
#split committee data into columns
	items = line.split("|")
	#the 6th column is transaction date
	transactionDate = items[5]
	#split date information MM/DD/YYYY HH:MM:SS at the space
	transactionDate = transactionDate.split(" ")
	#discard time data
	transactionDate = transactionDate[0]
	#split date
	transactionDate = transactionDate.split("/")
	#weed out null and atypical placeholder values (eg. 'N/A')
	if len(transactionDate) > 2:
		#create a datetime object. cast list values as integers and convert with datetime(YYYY, MM, DD, 0, 0)
		unixTransactionDate = datetime(int(transactionDate[2]), int(transactionDate[0]), int(transactionDate[1]), 0, 0)
		#take datetime object and convert into unix timestamp
		unixTransactionDate = calendar.timegm(unixTransactionDate.utctimetuple())
		#replace old date with unix timestamp
		items[5] = str(unixTransactionDate)
		#insert parsed year, month, day values as new fields
		items.insert(6, transactionDate[2])
		items.insert(7, transactionDate[0])
		items.insert(8, transactionDate[1])
	#select null and atypical placeholder values
	else:
		#normalize all to null
		items[5] = ""
		#insert empty fields for year, month, day values
		items.insert(6, "")
		items.insert(7, "")
		items.insert(8, "")
	#the 10th column is transaction amount
	transactionAmount = items[9]
	#split off $ sign from amount
	transactionAmount = transactionAmount.split("$")
	#discard $ sign
	transactionAmount = transactionAmount[1]
	#evaluate transactionAmount value for null or atypical place holder values
	if len(transactionAmount) < 4:
		#normalize null or atypical place holder values with 0 amount string
		transactionAmount = "0.00"
	if re.search("\)", transactionAmount):
		transactionAmount = re.sub("\)", "", transactionAmount)
		transactionAmount = "-" + transactionAmount
	#replace old transaction amount with formatted amount
	items[9] = transactionAmount
	if len(items[12]) < 1:
		items[12] = "0"
	memo = items[10]
	#join items list with |
	line = "|".join(items)
	#strip whatever line terminating symbol exists
	line = line.rstrip()	
	#write lines terminating with \n 
	transactionsFormat.write("%s\n" %(line))
	line = transactions.readline()
	if index%1000 == 0:
		transactions.flush()
		print index
