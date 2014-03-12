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
def getreport(committeeNameID, entityOneType, entityOneFirstName, entityOneLastName, cycleName, transactionType, startDate, endDate, download):
	#connect to database
	db = MySQLdb.connect(user=db_user, passwd=db_pass, db=db_db)
	cursor = db.cursor()	
	#variables
	committee = "you misspelled something somewhere"
	individualNames = "you misspelled something somewhere"
	candidateName = "you misspelled something somewhere"
	committeeName = "you misspelled something somewhere"
	individualTransaction = "you misspelled something somewhere"
	individualLine = "you misspelled something somewhere"
	report = []
	headers = "you misspelled something somewhere"
	recipient = "you misspelled something somewhere"
	transactions = "you misspelled something somewhere"
	#functions
	#search names by nameID, return candidate name
	def getCandidateName(index):
		if index <> 0:
			cursor.execute("select * from names where nameID = %s;",(index))
			name = gettuple(cursor.fetchall())
			name = name[3:5]
		else:
			name = [0,0]
		return name
	#search commitees by committeeID
	def getCommittee(index):
		cursor.execute("select * from committees where committeeID = %s;",(index))
		result = gettuple(cursor.fetchall())
		return result
	#search names by nameID, return all
	def getName(index):
		cursor.execute("select * from names where nameID = %s;",(index))
		result = gettuple(cursor.fetchall())
		return result
	#search transactions by either nameID or committeeID
	def getTransaction(subject, index):
		if subject == "individual":
			cursor.execute("select * from transactions where nameID = %s;",(index))
			transactions = cursor.fetchall()
		else:
			cursor.execute("select * from transactions where committeeID = %s;",(index))
			transactions = getlist(cursor.fetchall())
		return transactions
	#filter transactions by cycle
	def cycleFilter(index, cycleFilter, transactionList):
		individualFilter = []
		if len(transactionList[0]) >1:
			if cycleFilter <> "all":
				cursor.execute("select unixCycleBeginDate, unixCycleEndDate from cycles where cycleName = %s;",(cycleFilter))
				cycleDates = gettuple(cursor.fetchall())
				for line in transactionList:
					if (line[index] >= cycleDates[0]) and (line[index] <= cycleDates[1]):
						individualFilter.append(line)
				transactionList = individualFilter
				if len(transactionList) == 0:
					transactionList = [["Message 20: No transactions exist for selected cycle."]]
		return transactionList
	#filter transactions by date range
	def dateFilter(index, userFilter, filterType, transactionList):
		if userFilter:
			if len(transactionList[0]) > 1:
				individualFilter = []
				dateTmp = userFilter.split("/")
				if (len(dateTmp[0]) == 2) and (len(dateTmp[1]) == 2) and (len(dateTmp[2]) == 4):
					dateTmp = datetime(int(dateTmp[2]),int(dateTmp[0]),int(dateTmp[1]),0,0)
					dateTmp = calendar.timegm(dateTmp.utctimetuple())
					for line in transactionList:
						if filterType == "start":
							if line[index] >= dateTmp:
								individualFilter.append(line)
						if filterType == "end":
							if line[index] <= dateTmp:
								individualFilter.append(line)
					transactionList = individualFilter
				else:
					transactionList = [["Message 10: Invalid date format."]]
			if len(transactionList) == 0:
				transactionList = [["Message 21: no transactions exist for given date(s)."]]
		return transactionList
	#filter transactions by type
	def transactionFilter(index, userFilter, transactionList):
		if userFilter <> "all":
			if len(transactionList[0]) > 1:
				individualFilter = []
				for line in transactionList:
					if line[index] == userFilter:
						individualFilter.append(line)
				transactionList = individualFilter
				if len(transactionList) == 0:
					transactionList = [["Message 17: No such expenses exist for this committee."]]
		return transactionList
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
				#use getTransaction
				individualTransaction = getTransaction("individual", line[0])
				#if there is more than one transaction relating to this nameID
				if len(individualTransaction) > 1:
					#make individualTransactions a list of lists	
					individualTransaction = getlist(individualTransaction)
					#for each transaction
					for instance in individualTransaction:
						#use getCommittee to retrieve committee informatiion for transaction
						committee = getCommittee(instance[4])
						#use getCandidateName ''
						candidateName = getCandidateName(committee[4])
						#use getName ''
						committeeName = getName(committee[1])
						#create a list that contains only the information corresponding to column headers in report
						individualLine = [line[2]] + [line[4]] + [line[3]] + line[5:12] + line[13:15] + [committeeName[3]] + [candidateName[1]] + [candidateName[0]] + committee[31:33] + [committee[34]] + [instance[3]] + [instance[5]] + [instance[9]] + instance[13:15]
						#append this line to report
						report.append(individualLine)
				#if there is only one transaction associated with each individual
				if len(individualTransaction) == 1:
					#turn the transaction information into a list
					individualTransaction = gettuple(individualTransaction)
					committee = getCommittee(individualTransaction[4])
					candidateName = getCandidateName(committee[4])
					committeeName = getName(committee[1])
					#create a list that contains only the information corresponding to column headers in report
					individualLine = [line[2]] + [line[4]] + [line[3]] + line[5:12] + line[13:15] + [committeeName[3]] + [candidateName[1]] + [candidateName[0]] + committee[31:33] + [committee[34]] + [individualTransaction[3]] + [individualTransaction[5]] + [individualTransaction[9]] + individualTransaction[13:15]
					#append this line to report
					report.append(individualLine)
				#If for some reason there are no associated transactions which is tech. possible, inform the user
				if len(report) == 0:
					report = [["Message 1: No transactions found."]]
		#in the event that there is only one individual that matches the partial first and last name
		elif len(individualNames) == 1:
			#turn that result into a list
			individualNames = gettuple(individualNames)
			individualTransaction = getTransaction("individual", individualNames[0])
			#if there is more than one transaction associated with that individual, follow the corresponding proceedures as detailed above
			if len(individualTransaction) > 1:
				individualTransaction = getlist(individualTransaction)
				for instance in individualTransaction:
					committee = getCommittee(instance[4])
					candidateName = getCandidateName(committee[4])
					committeeName = getName(committee[1])
					individualLine = [individualNames[2]] + [individualNames[4]] + [individualNames[3]] + individualNames[5:12] + individualNames[13:15] + [committeeName[3]] + [candidateName[1]] + [candidateName[0]] + committee[31:33] + [committee[34]] + [instance[3]] + [instance[5]] + [instance[9]] + instance[13:15]
					report.append(individualLine)
			#if there is only one transaction associated with that individual, follow the corresponding proceedures as detailed above
			if len(individualTransaction) == 1:
				individualTransaction = gettuple(individualTransaction)
				committee = getCommittee(individualTransaction[4])
				candidateName = getCandidateName(committee[4])
				committeeName = getName(committee[1])
				individualLine = [individualNames[2]] + [individualNames[4]] + [individualNames[3]] + individualNames[5:12] + individualNames[13:15] + [committeeName[3]] + [candidateName[1]] + [candidateName[0]] + committee[31:33] + [committee[34]] + [individualTransaction[3]] + [individualTransaction[5]] + [individualTransaction[9]] + individualTransaction[13:15]
				report.append(individualLine)
			#if for some reason the name has no related transactions which is technically possible I guess, inform the user
			if len(report) == 0:
				report = [["Message 2: No transactions found."]]
		#If there is no individual that matches the partial first and last name, inform the user
		elif len(individualNames) == 0:
			report = [["Message 3: Individual not found."]]
		if len(report) <> 0:
			#time filter:
			report = cycleFilter(19, cycleName, report)
			report = dateFilter(19, startDate, "start", report)
			report = dateFilter (19, endDate, "end", report)
			#use transactionFilter to apply user option
			report = transactionFilter(18, transactionType, report)
			if len(report[0]) > 1:
				for line in report:
					line[19] = datetime.fromtimestamp(line[19]).strftime('%m-%d-%Y')
		report.insert(0, headers)
		report.insert(0, [entityOneFirstName, entityOneLastName])
	#End individual query 
	if entityOneType == "committee":
		#use getName to get name information for ID from form
		committee = getCommittee(committeeNameID)
		#make sure the committee exists (no errors in inputting the id)
		if len(committee) > 0:
			#use getCommittee
			committeeName = getName(committee[1])
			#get transactions
			transactions = getTransaction("committee", committee[0])
			#set up report column headings
			headers = ['Committee Type','Committee Name', 'Committee Party', 'Committee Office', 'Incumbent: 1 = Yes', 'Transaction Type', 'Transaction Date', 'Transaction Amount', 'Transaction Memo', 'Transaction Category Name', 'Contributor/Payee Type', 'C/P First Name', 'C/P Last Name', 'C/P Address 1', 'C/P Address 2', 'C/P City', 'C/P State', 'C/P Zipcode', 'C/P Occupation', 'C/P Employer']
			for line in transactions:
				#use getName to get contributor or payee involved in each transaction
				recipient = getName(line[10])		
				for i in range(0,len(recipient)):
					recipient[i] = str(recipient[i])
					recipient[i] = unicode(recipient[i], "ISO-8859-1")
				#build list that contains only the information referenced in the report headings
				committeeTransaction = committeeName[2:4] + committee[31:33] + [committee[34]] + [line[3]] + [line[5]] + [line[9]] + line[13:15] + [recipient[2]] + [recipient[4]] + [recipient[3]] + recipient[7:12] + recipient[13:15]
				#append that new line to reports
				report.append(committeeTransaction)
			if len(report) <> 0:
				#Filters
				report = cycleFilter(6, cycleName, report)
				report = dateFilter(6, startDate, "start", report)
				report = dateFilter (6, endDate, "end", report)
				report = transactionFilter(5, transactionType, report)
				if len(report[0]) > 1:
					for line in report:
						line[6] = datetime.fromtimestamp(line[6]).strftime('%m-%d-%Y')
			report.insert(0,headers)
			report.insert(0,[committeeNameID])
	db.commit()
	cursor.close()
	return report
