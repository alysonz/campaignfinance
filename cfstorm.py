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
from storm.locals import *
from storm.tracer import debug
import sys
import json



#Database connection
database = create_database("mysql://%s:%s@localhost/%s"%(db_user, db_pass, db_db))
store = Store(database)



#Classes
class Names(object):
	__storm_table__ = "names"
	nameID = Int(primary=True)
	nameGroupID = Int()
	entityTypeName = Unicode()
	lastName = Unicode()
	firstName = Unicode()
	middleName = Unicode()
	suffix = Unicode()
	address1 = Unicode()
	address2 = Unicode()
	city = Unicode()
	state = Unicode()
	zipcode = Unicode()
	countyName = Unicode()
	occupation = Unicode()
	employer = Unicode()

class Cycles(object):
	__storm_table__ = "cycles"
	cycleID = Int(primary=True)
	cycleName = Int()
	unixCycleBeginDate = Int()
	cycleBeginYear = Int()
	cycleBeginMonth = Int()
	cycleBeginDay = Int()
	unixCycleEndDate = Int()
	cycleEndYear = Int()
	cycleEndMonth = Int()
	cycleEndDay = Int()

class Transactions(object):
	__storm_table__ = "transactions"
	transactionID = Int(primary=True)
	modifiesTransactionID = Int()
	transactionTypeName = Unicode()
	incomeExpenseNeutral = Unicode()
	committeeID = Int()
	unixTransactionDate = Int()
	transactionYear = Int()
	transactionMonth = Int()
	transactionDay = Int()
	amount = Float()
	nameID = Int()
	isForBenefit = Unicode()
	subjectCommitteeID = Int()
	memo = Unicode()
	categoryName = Unicode()

class Committees(object):
	__storm_table__ = "committees"
	committeeID = Int(primary=True)
	nameID = Int()
	chairpersonNameID = Int()
	treasurerNameID = Int()
	candidateNameID = Int()
	designeeNameID = Int()
	sponsorNameID = Int()
	ballotMeasureID = Int()
	sosIdentifier = Unicode()
	measureNumber = Int()
	shortTitle = Unicode()
	officialTitle = Unicode()
	physicalAddress1 = Unicode()
	physicalAddress2 = Unicode()
	physicalCity = Unicode()
	physicalState = Unicode()
	physicalZipcode = Unicode()
	sponsorType = Unicode()
	sponsorRelationship = Unicode()
	unixOrganizationDate = Int()
	organizationYear = Int()
	organizationMonth = Int()
	organizationDay = Int()
	unixTerminationDate = Int()
	terminationYear = Int()
	terminationMonth = Int()
	terminationDay = Int()
	benefitsBallotMeasure = Unicode()
	financialInstitution1 = Unicode()
	financialInstitution2 = Unicode()
	financialInstitution3 = Unicode()
	partyName = Unicode()
	officeName = Unicode()
	countyName = Unicode()
	candidateIsIncumbent = Unicode()
	cycleName = Int()
	unixCycleBeginDate = Int()
	cycleBeginYear = Int()
	cycleBeginMonth = Int()
	cycleBeginDay = Int()
	unixCycleEndDate = Int()
	cycleEndYear = Int()
	cycleEndMonth = Int()
	cycleEndDay = Int()
	candidateOtherPartyName = Unicode()



headers = ["Transaction Date","Committee Type", "Committee Name", "Candidate First Name", "Candidate Last Name", "Party", "Office", "Transaction Amount", "Transaction Type", "Transaction Memo", "Transaction Category", "Contributor/Payee Type", "C/P First Name", "C/P Last Name", "C/P Middle Name", "C/P Suffix", "C/P Address", "C/P City", "C/P State", "C/P Zipcode", "C/P Occupation", "C/P Employer"]



#Queries
def committeeQuery(committeeID):
	committeeID = int(committeeID)
	report = []
	getCommittee = store.find(Committees, Committees.committeeID == committeeID)
	getCandidate = store.find(Names, Names.nameID == getCommittee[0].candidateNameID)
	getCommitteeName = store.find(Names, Names.nameID == getCommittee[0].nameID)
	getTransactions = store.find(Transactions, Transactions.committeeID == getCommittee[0].committeeID)
	for transaction in getTransactions:
		getContributor = store.find(Names, Names.nameID == transaction.nameID)
		record = [transaction.unixTransactionDate, getCommitteeName[0].entityTypeName, getCommitteeName[0].lastName, getCandidate[0].firstName, getCandidate[0].lastName, getCommittee[0].partyName, getCommittee[0].officeName, transaction.amount, transaction.incomeExpenseNeutral, transaction.memo, transaction.categoryName, getContributor[0].entityTypeName, getContributor[0].firstName, getContributor[0].lastName, getContributor[0].middleName, getContributor[0].suffix, getContributor[0].address1 + " " + getContributor[0].address2, getContributor[0].city, getContributor[0].state, getContributor[0].zipcode, getContributor[0].occupation, getContributor[0].employer]
		report.append(record)
	return report



def individualQuery(lastName, firstName):
	report = []
	getName = store.find(Names, Names.lastName.like(u"%%%s%%"%(lastName)), Names.firstName.like(u"%%%s%%"%(firstName)))
	if getName.count() > 0:
		for line in getName:
			getTransactions = store.find(Transactions, Transactions.nameID==line.nameID)
			if getTransactions.count() > 0:
				for transaction in getTransactions:
					getCommittee = store.find(Committees, Committees.committeeID == transaction.committeeID)
					getCandidate = store.find(Names, Names.nameID == getCommittee[0].candidateNameID)
					getCommitteeName = store.find(Names, Names.nameID == getCommittee[0].nameID)
					record = [transaction.unixTransactionDate, getCommitteeName[0].lastName, getCandidate[0].firstName, getCandidate[0].lastName, getCommittee[0].partyName, getCommittee[0].officeName, transaction.amount, transaction.incomeExpenseNeutral, transaction.memo, transaction.categoryName, line.entityTypeName, line.firstName, line.lastName, line.middleName, line.suffix, line.address1 + " " + line.address2, line.city, line.state, line.zipcode, line.occupation, line.employer]
					report.append(record)
	else:
		report.append(["Individual not found"])
	return report



#Filters
def convertDate(report):
	try:
		for line in report:
			line[0] = datetime.fromtimestamp(line[0]).strftime('%m-%d-%Y')
		report.insert(0, headers)
	except (TypeError):
		pass
	return report



def cycle(cycle, report):
	cycle = int(cycle)
	reportFiltered = []
	cycleRange = store.find(Cycles, Cycles.cycleName == cycle)
	for line in report:
		if line[0] >= unixCycleBeginDate and line[0] <= unixCycleEndDate:
			reportFiltered.append(line)
	if len(reportFiltered) < 1:
		return reportFiltered
	else:
		reportFiltered = [["No records exist for cycle provided."]]
		return reportFiltered



def date(date, dateType, report):
	reportFiltered = []
	if date:
		date = date.split("/")
		if len(date[2]) != 4:
			reportFiltered = [["Invalid date format."]]
		try:
			unixDate = datetime(int(date[2]),int(date[0]),int(date[1]),0,0)
			unixDate = calendar.timegm(unixDate.utctimetuple())
			for line in report:
				if (dateType == "begin") and (line[0] >= unixDate):
						reportFiltered.append(line)
				elif dateType == "end" and (line[0] <= unixDate):
						reportFiltered.append(line)
		except (IndexError):
			reportFiltered = [["Invalid date format."]]
	if len(reportFiltered) < 1:
		reportFiltered = [["No records exist for date range provided."]]
	return reportFiltered



def incomeExpense(transactionType, report):
	reportFiltered = []
	for line in report:
		if line[8] == transactionType:
			reportFiltered.append(line)
	if len(reportFiltered) < 1:
		reportFiltered = [["No %s transactions exist."%(transactionType)]]
	return reportFiltered



