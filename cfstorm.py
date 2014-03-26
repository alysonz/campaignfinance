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
database = create_database("mysql://%s:%s@localhost/%s"%(db_user, db_pass, db_db))

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
	officName = Unicode()
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

store = Store(database)

last = "asdfg"
first = ""
getname = store.find(Names, Names.lastName.like(u"%%%s%%"%(last)), Names.firstName.like(u"%%%s%%"%(first)))

report = []

if getname.count > 1:
	for line in getname:
		gettransactions = store.find(Transactions, Transactions.nameID==line.nameID)
		for item in gettransactions:
			getcommittee = store.find(Names, Names.nameID==item.committeeID)
#		record = [line.entityTypeName, line.firstName, line.lastName, line.middleName, line.suffix, line.address1, line.address2, line.city, line.state, line.zipcode, line.occupation, line.employer, getcommittee.lastName, 
else:
	report = [["Individual not found"]]

test = store.find(Names, Names.lastName==u'mcdermott')
