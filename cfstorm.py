#!/usr/bin/python
#import resources
import MySQLdb
import re
from datetime import datetime
import calendar
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

def compileRow(committeeObject):
	getCommitteeName = store.find(Names, Names.nameID == committeeObject.nameID)
	getCandidate = store.find(Names, Names.nameID == committeeObject.candidateNameID)
	candidateName = getCandidate[0].firstName + ' ' + getCandidate[0].lastName
	record = {'committeeID': committeeObject.committeeID, 'committeeName': getCommitteeName[0].lastName, 'candidateName': candidateName,  'cycle': committeeObject.cycleName}
	return record

#Queries

#queryBy
def queryByRace(race, cycleName):
	race = unicode(race)
	cycleName = int(cycleName)
	report = []
	getCommittees = store.find(Committees, Committees.officeName == race, Committees.cycleName == cycleName)
	for committee in getCommittees:
		report.append(compileRow(committee))
	if len(report) > 0:
		return report
	else:
		report = False
		return report



def queryByCandidate(firstName, lastName):
	report = []
	getNames = store.find(Names, Names.lastName.like(u"%%%s%%"%(lastName)), Names.firstName.like(u"%%%s%%"%(firstName)))
	for name in getNames:
		getCommittee = store.find(Committees, Committees.candidateNameID == name.nameID)
		try:
			report.append(compileRow(getCommittee[0]))
		except IndexError:
			pass
	if len(report) > 0:
		return report
	else:
		report = False
		return report



def queryByCommittee(committee):
	report = []
	getNames = store.find(Names, Names.lastName.like(u"%%%s%%"%(committee)))
	for name in getNames:
		getCommittee = store.find(Committees, Committees.nameID == name.nameID)
		try:
			report.append(compileRow(getCommittee[0]))
		except IndexError:
			pass
	if len(report) > 0:
		return report
	else:
		report = False
		return report



#getData
def committeeQuery(committeeID, cycle, download):
	request = []
	for committee in committeeID:
		committee = int(committee)
		getCommittee = store.find((Committees.committeeID, Committees.nameID, Committees.candidateNameID, Committees.partyName, Committees.officeName), Committees.committeeID == committee)
		getCandidate = store.find((Names.firstName, Names.lastName), Names.nameID == getCommittee[0][2])
		getCommitteeName = store.find((Names.entityTypeName, Names.lastName), Names.nameID == getCommittee[0][1])
		if (download=='True'):
			if cycle != 'All':
				cycleRange = store.find((Cycles.unixCycleBeginDate, Cycles.unixCycleEndDate), Cycles.cycleName == int(cycle))
				getTransactions = store.find((Transactions.unixTransactionDate, Transactions.amount, Transactions.incomeExpenseNeutral, Transactions.memo, Transactions.categoryName, Transactions.nameID), And(Transactions.committeeID == getCommittee[0][0], Transactions.unixTransactionDate >= cycleRange[0][0], Transactions.unixTransactionDate <= cycleRange[0][1]))
			else:
				getTransactions = store.find((Transactions.unixTransactionDate, Transactions.amount, Transactions.incomeExpenseNeutral, Transactions.memo, Transactions.categoryName, Transactions.nameID), Transactions.committeeID == getCommittee[0][0])
		else:
			if cycle != 'All':
				cycleRange = store.find((Cycles.unixCycleBeginDate, Cycles.unixCycleEndDate), Cycles.cycleName == int(cycle))
				getTransactions = store.find(Transactions, And(Transactions.committeeID == getCommittee[0][0], Transactions.unixTransactionDate >= cycleRange[0][0], Transactions.unixTransactionDate <= cycleRange[0][1]))
				getTransactions = [(transaction.unixTransactionDate, transaction.amount, transaction.incomeExpenseNeutral, transaction.memo, transaction.categoryName, transaction.nameID) for transaction in getTransactions.order_by(Transactions.unixTransactionDate)[:100]]
			else:
				getTransactions = store.find(Transactions, Transactions.committeeID == getCommittee[0][0])
				getTransactions = [(transaction.unixTransactionDate, transaction.amount, transaction.incomeExpenseNeutral, transaction.memo, transaction.categoryName, transaction.nameID) for transaction in getTransactions.order_by(Transactions.unixTransactionDate)[:100]]
		report = {'committeeID': getCommittee[0][0], 'committeeName': getCommitteeName[0][1], 'transactions': []}
		for transaction in getTransactions:
			getContributor = store.find((Names.entityTypeName, Names.firstName, Names.lastName, Names.middleName, Names.suffix, Names.address1, Names.address2, Names.city, Names.state, Names.zipcode, Names.occupation, Names.employer), Names.nameID == transaction[5])
			record = [transaction[0], getCommitteeName[0][0], getCommitteeName[0][1], getCandidate[0][0], getCandidate[0][1], getCommittee[0][3], getCommittee[0][4], transaction[1], transaction[2], transaction[3], transaction[4], getContributor[0][0], getContributor[0][1], getContributor[0][2], getContributor[0][3], getContributor[0][4], getContributor[0][5] + " " + getContributor[0][6], getContributor[0][7], getContributor[0][8], getContributor[0][9], getContributor[0][10], getContributor[0][11]]
			report['transactions'].append(record)
		request.append(report)
	return request



def individualQuery(lastName, firstName):
	request = []
	report = {'committeeID': firstName+lastName, 'committeeName': firstName+' '+lastName, 'transactions': []}
	getName = store.find(Names, Names.lastName.like(u"%%%s%%"%(lastName)), Names.firstName.like(u"%%%s%%"%(firstName)))
	if getName.count() > 0:
		for line in getName:
			getTransactions = store.find(Transactions, Transactions.nameID==line.nameID)
			if getTransactions.count() > 0:
				for transaction in getTransactions:
					getCommittee = store.find(Committees, Committees.committeeID == transaction.committeeID)
					getCandidate = store.find(Names, Names.nameID == getCommittee[0].candidateNameID)
					getCommitteeName = store.find(Names, Names.nameID == getCommittee[0].nameID)
					record = [transaction.unixTransactionDate, getCommitteeName[0].entityTypeName, getCommitteeName[0].lastName, getCandidate[0].firstName, getCandidate[0].lastName, getCommittee[0].partyName, getCommittee[0].officeName, transaction.amount, transaction.incomeExpenseNeutral, transaction.memo, transaction.categoryName, line.entityTypeName, line.firstName, line.lastName, line.middleName, line.suffix, line.address1 + " " + line.address2, line.city, line.state, line.zipcode, line.occupation, line.employer]
					report['transactions'].append(record)
	else:
		report['transactions'].append(["Individual not found"])
	request.append(report)
	return request



#Filters
def convertDate(report):
	for item in report:
		try:
			for line in item['transactions']:
				line[0] = datetime.fromtimestamp(line[0]).strftime('%m-%d-%Y')
			item['transactions'].insert(0, headers)
		except (TypeError):
			pass
	return report



def cycle(cycle, report):
	cycle = int(cycle)
	reportFiltered = []
	cycleRange = store.find(Cycles, Cycles.cycleName == cycle)
	for item in report:
		for line in item['transactions']:
			if line[0] >= cycleRange[0].unixCycleBeginDate and line[0] <= cycleRange[0].unixCycleEndDate:
				reportFiltered.append(line)
		if len(reportFiltered) > 0:
			item['transactions'] = reportFiltered
		else:
			item['transactions'] = [["No records exist for cycle provided."]]
	return report



def date(date, dateType, report):
	if date:
		date = date.split("/")
		if len(date[2]) != 4:
			reportFiltered = [["Invalid date format."]]
		try:
			unixDate = datetime(int(date[2]),int(date[0]),int(date[1]),0,0)
			unixDate = calendar.timegm(unixDate.utctimetuple())
			for item in report:
				for line in item['transactions']:
					if (dateType == "begin") and (line[0] >= unixDate):
							reportFiltered.append(line)
					elif dateType == "end" and (line[0] <= unixDate):
							reportFiltered.append(line)
		except (IndexError):
			for item in report:
				reportFiltered = [["Invalid date format."]]
	if len(reportFiltered) < 1:
		reportFiltered = [["No records exist for date range provided."]]
	for item in report:
		item['transactions'] = reportFiltered
	return report



def incomeExpense(transactionType, report):
	reportFiltered = []
	for item in report:
		for line in item['transactions']:
			if line[8] == int(transactionType):
				reportFiltered.append(line)
		if len(reportFiltered) < 1:
			reportFiltered = [["No %s transactions exist."%(transactionType)]]
		item['transactions'] = reportFiltered
	return report



