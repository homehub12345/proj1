from SQL_Types import force,S_String,S_Int_z,S_Int_a,S_Date_z,S_Date_a,S_SDate_z, S_SDate_a

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Integer, ForeignKey, String, Column, Date, Float, NVARCHAR, ForeignKeyConstraint, collate
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
Base = declarative_base()


        

class User(Base):
    #User class will be merged with ArContact later
    __tablename__ = 'MC_SfContact_AppStatus'
    __table_args__ = {'schema':'AdHoc.dbo'}
    SalesforceContactId = Column(String, primary_key=True)
    OperationStatusId = Column(Integer)
    

class ArContact(Base):
    __tablename__ = 'ArContact'
    __table_args__ = {'schema':'RawData.dbo'}#, 'collation':'SQL_Latin1_General_CP1_CI_AS'}
    SalesforceContactId = Column(NVARCHAR(32, collation='Latin1_General_CI_AS'))
    ArReportId = Column(Integer, primary_key = True)
    #history: works
    history = relationship("ArCreditHistory", backref = "ArContact",lazy='subquery')
    inquiry = relationship("ArInquiry", backref = "ArContact",lazy='subquery')
    #score = relationship("ArCreditScore", backref = "ArContact",lazy='subquery')
    res = relationship("ArResidence", backref = "ArContact",lazy='subquery')
    rec = relationship("ArPublicRecord", backref = "ArContact",lazy='subquery')
    emp = relationship("ArEmployer", backref = "ArContact",lazy='subquery')

class ArCreditHistory(Base):
    __tablename__ = 'ArCreditHistory'
    __table_args__ = {'schema':'RawData.dbo'}
    ArReportId = Column(Integer, ForeignKey('RawData.dbo.ArContact.ArReportId'), primary_key=True)
    ThirtyDaysLate = Column(S_Int_z)
    SixtyDaysLate = Column(S_Int_z)
    NinetyDaysLate = Column(S_Int_z)
    PaymentPattern =  Column(S_String)
    PaymentPatternStartDate = Column(S_SDate_a)
    AccountOpenedDate = Column(S_SDate_a)
    AccountClosedDate = Column(S_SDate_a) 
    AccountReportedDate = Column(S_SDate_a)
    LastActivityDate = Column(S_SDate_a)
    AccountStatusDate = Column(S_SDate_a)
    AccountOwnershipType = Column(S_String)
    AccountStatus = Column(S_String) 
    AccountType = Column(S_String)
 #   BusinessType = Column(S_String)
    LoanType = Column(S_String)
    MonthsReviewed = Column(S_Int_a)
    CreditLimit = Column(S_Int_z)
    HighestBalanceAmount = Column(S_Int_z)
    MonthlyPayment = Column(S_Int_z)
    UnpaidBalance = Column(S_Int_a)
    TermsDescription = Column(S_String)
    TermsMonthsCount = Column(S_Int_a)

    #Latenesses below: exclude when using lateness model
    #CurrentRatingCode = Column(S_String)
    #CurrentRatingType = Column(S_String)
    #HighestAdverseCode = Column(S_Int_z)
    #HighestAdverseDate = Column(S_SDate_a)
    #HighestAdverseType = Column(S_String)
    #RecentAdverseCode = Column(S_Int_z)
    #RecentAdverseDate = Column(S_SDate_a)
    #RecentAdverseType = Column(S_String)
    #PriorAdverseCode = Column(S_Int_z)
    #PriorAdverseDate = Column(S_SDate_a)
    #PriorAdverseType = Column(S_String)

    ArCreditLiabilityId = Column(String, primary_key=True)
    #comments = relationship("ArCreditHistoryComment", 
    	#                    backref = "ArCreditHistory", 
    	#                    lazy='subquery')

class ArInquiry(Base):
    __tablename__ = 'ArInquiry'
    __table_args__ = {'schema':'RawData.dbo'}
    ArReportId = Column(S_Int_z, ForeignKey('RawData.dbo.ArContact.ArReportId'), primary_key=True)
    InquiryDate = Column(S_SDate_a, primary_key=True)


#class ArCreditHistoryComment(Base):
#    __tablename__ = 'ArCreditHistoryComment'
#    __table_args__ = {'schema':'RawData.dbo'}
#    ArCreditLiabilityId = Column(String, 
#    							ForeignKey(
#    								'RawData.dbo.ArCreditHistory.ArCreditLiabilityId'
#    								), 
#    							primary_key=True)
#    Comment = Column(S_String)
#    CommentCode = Column(S_String, primary_key=True)


class ArCreditScore(Base):
	__tablename__ = 'ArCreditScore'
	__table_args__ = {'schema':'RawData.dbo'}
	ArReportId = Column(S_Int_z, ForeignKey('RawData.dbo.ArContact.ArReportId'), primary_key=True)
	ArScoreId = Column(S_String)
	Score = Column(S_Int_z)
	ScoreDate = Column(S_SDate_a, primary_key=True)
	score_factors = relationship("ArScoreFactor", backref="ArCreditScore",
								 lazy='subquery')

class ArScoreFactor(Base):
	__tablename__ = 'ArScoreFactor'
	__table_args__ = {'schema':'RawData.dbo'}
	ArReportId = Column(S_Int_z, ForeignKey('RawData.dbo.ArCreditScore.ArReportId'), primary_key=True)
	ReasonCode = Column(S_Int_z, primary_key=True)

class ArResidence(Base):
	__tablename__ = 'ArResidence'
	__table_args__ = {'schema':'RawData.dbo'}
	ArReportId = Column(S_Int_z, ForeignKey('RawData.dbo.ArContact.ArReportId'), primary_key=True)
#	State = Column(S_String)
#	Zip = Column(S_Int_z)
	MonthsAtResidence = Column(S_Int_a)
	YearsAtResidence = Column(S_Int_a)
#	CurrentResidence = Column(S_Int_a)
#	Address = Column(S_String)

class ArPublicRecord(Base):
    __tablename__ = 'ArPublicRecord'
    __table_args__ = {'schema':'RawData.dbo'}
    ArReportId = Column(S_Int_z, ForeignKey('RawData.dbo.ArContact.ArReportId'), primary_key=True)
    RecordType = Column(S_String)
#   RecordTypeOther = Column(S_String)
#   CourtName = Column(S_String)
    DispositionType = Column(S_String)
    DispositionDate = Column(S_SDate_z)
#	FiledDate = Column(S_SDate_a)
#	ReportedDate = Column(S_SDate_a, primary_key=True)
#	SettledDate = Column(S_SDate_z)
    BankruptcyLiabilitiesAmount = Column(S_Int_z)
#	DisputeFlag = Column(S_Int_z)
#	Offense = Column(S_String)
#	DegreeofOffense = Column(S_String)
    MonthsSentencedTo = Column(S_Int_z)
    YearsSentencedTo = Column(S_Int_z) 
    LegalObligationAmount = Column(S_Int_z)
#	YearsProbation = Column(S_Int_z)
#	MonthsProbation = Column(S_Int_z) 
#	CrimTypeSourceCode = Column(S_Int_z)
#	TypeOfOffense = Column(S_Int_z)

class ArEmployer(Base):
	__tablename__ = 'ArEmployer'
	__table_args__ = {'schema':'RawData.dbo'}
	ArReportId = Column(S_Int_z, ForeignKey('RawData.dbo.ArContact.ArReportId'), primary_key=True)
#	CompanyName = Column(S_String, primary_key = True)
#	Position = Column(S_String)
	CurrentEmployer = Column(S_Int_z)
	SelfEmployed = Column(S_Int_z)