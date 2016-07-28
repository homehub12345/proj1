
#SO PRETTY :D :D

class QueryData():
    def __init__(self):
        self.rmv = ["SalesforceContactId", "ArReportId", "ArCreditLiabilityId", "ThirtyDaysLate", "SixtyDaysLate", "NinetyDaysLate"]
        
        self.subquery_names = []

        self.history = ("ATTR history FLAG" 
         "|STR PaymentPattern AccountOwnershipType AccountStatus AccountType "
           + "BusinessType LoanType TermsDescription CurrentRatingCode "
           + "CurrentRatingType HighestAdverseType RecentAdverseType "
           + "PriorAdverseType"
           "|AVD ArReportId ArCreditLiabilityId ThirtyDaysLate SixtyDaysLate NinetyDaysLate"
        #    "Comment_^_mode CommentCode_^_mode"
    	   #  "|AVD ArReportId ArCreditLiabilityId comments ThirtyDaysLate, SixtyDaysLate, NinetyDaysLate"
       #   "|SUBQRMV comments"
          "|EXISTSM late ThirtyDaysLate SixtyDaysLate NinetyDaysLate")

        self.inquiry = ("ATTR inquiry" +
    	     "|AVD ArReportId")

        #self.ArCommentHandling = ("ATTR comments" +
    		# "|STR Comment CommentCode|AVD ArReportId ArCreditLiabilityId")

        #self.credit_score = ("ATTR score FLAG"
    		# "|AVD ArReportId ArScoreId score score_factors"
         # "|SUBQ score_factors"
         #  )

        self.ArResidence = ("ATTR res"
    		 +"|EXISTS CurrentResidence"
    		 +"|AVD ArReportId State Zip Address")

        self.ArPublicRecord = ("ATTR rec"
    		 +"|STR RecordType RecordTypeOther Courtname Offense DegreeofOffense"
           "DispositionType"
    		 +"|AVD ArReportId")

        self.ArEmployer = ("ATTR emp"
    		 +"|STR CompanyName Position"
    		 +"|EXISTS CurrentEmployer SelfEmployed|AVD ArReportId")
       
        self.User = ("ATTR __self__"
          +"|SUBQ records")
       
        #self.ArContact = ("ATTR __self__|SUBQ history inquiry score res rec emp")
       #note: SCORE originally under SUBQ but since removed
        self.ArContact = ("ATTR __self__|SUBQ history|SUBQRMV inquiry res rec emp")
        self.ArContactHandling = (self.history + '\n' +
    						    self.inquiry + '\n' +
    						    #self.credit_score + '\n' +
    						    self.ArResidence + '\n' +
    						    self.ArPublicRecord + '\n' +
    						    self.ArEmployer + '\n' +
                               self.ArContact)
	