
# QueryData: Contains strings to determine how aggregate attributes should be
# constructed, how lists of subclasses should be handled, and how
# the dictionary should be collapsed.

class QueryData():
    def __init__(self):
        #self.rmv: list of attributes to be removed if encountered while 
        #the dictionaries are being collapsed.
        self.rmv = ["SalesforceContactId", "ArReportId", "ArCreditLiabilityId"]
        
        self.subquery_names = []


        # string syntax:
        #     ATTR [AttrField1] [AttrField2]
        #
        #     [AttrField1]: The attribute on the parent object in which the
        #     list of classes that are to be aggregated into new data are 
        #     contained.
        #
        #     If [AttrField1] is __self__ the parent object itself is to be the
        #     thing modified, and only by removing or expanding subqueries.
        # 
        #     If [AttrField2] is present, this signals that for each object
        #     in the list contained by parent_object.[AttrField1], operations 
        #     are to be performed by removing or expanding subqueries.
        #
        #     STR [Fields]:  For each [strfield] in [Fields], this signals that
        #     new fields based on the mode of [strfield] in class instances 
        #     contained within parent_object.[AttrField1] are to be placed 
        #     in parent_object.  
        #     ^: For use with string/label data.
        #
        #     AVD [Fields]: For each [avdfield] in [Fields] no processing will
        #     be performed and no new aggregate fields will be placed in
        #     parent_object
        #
        #     EXISTS [Fields]: For each [efield] in [Fields], this signals that
        #     one new field based on whether or not there exists an instance of 
        #     [efield] for all class instances contained within 
        #     parent_object.[AttrField1] for which its value is not numpy.nan
        #     or zero (that is to say, for which data for the field exists).
        #
        #     EXISTSM [new_name] [Fields]: Similar to Exists, but adds only a 
        #     single field [new_name] based on whether or not data exists
        #     for any of the [efield] in [fields].
        #
        #     SUBQ [fields]: For each [field] in [fields], replaces the list of
        #     classes contained within attribute [field] with dictionaries.
        #
        #     SUBQRMV [fields]: For each [field] in [fields], removes the list
        #     of classes contained within attribute [field] by removing
        #     attribute [field] altogether.
        #
        #     In the event that a field is NOT specified by STR or 
        #     EXISTS or AVD:
        #         
        #         -Its sum, max, min, std, median, mean, and variance
        #         for that field are to all be added as fields to the
        #         parent_object.
        #
        #         -This is the case with float, integer, and date data.
        #         
    

        #self.history: controls how new aggregate attributes 
        #              are formed from history data.
        self.history = ("ATTR history FLAG" 
         "|STR PaymentPattern AccountOwnershipType AccountStatus AccountType "
           + "BusinessType LoanType TermsDescription CurrentRatingCode "
           + "CurrentRatingType HighestAdverseType RecentAdverseType "
           + "PriorAdverseType"
           "|AVD ArReportId ArCreditLiabilityId"
        #    "Comment_^_mode CommentCode_^_mode"
    	   #  "|AVD ArReportId ArCreditLiabilityId comments ThirtyDaysLate, SixtyDaysLate, NinetyDaysLate"
       #   "|SUBQRMV comments"
          "|EXISTSM late ThirtyDaysLate SixtyDaysLate NinetyDaysLate")


        self.inquiry = ("ATTR inquiry" +
    	     "|AVD ArReportId")

        #self.ArCommentHandling = ("ATTR comments" +
    		# "|STR Comment CommentCode|AVD ArReportId ArCreditLiabilityId")

        self.credit_score = ("ATTR score FLAG"
    		 "|AVD ArReportId ArScoreId score score_factors"
          "|SUBQ score_factors"
           )

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
       
        self.ArContact = ("ATTR __self__|SUBQ history score inquiry"
          +"|SUBQRMV res rec emp")

        self.ArContactHandling = (self.history + '\n' +
                    self.inquiry + '\n' +
                    self.credit_score + '\n' +
                    self.ArResidence + '\n' +
                    self.ArPublicRecord + '\n' +
                    self.ArEmployer + '\n' +
                               self.ArContact)
	