from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib

from SQL_Hierarchy import ArContact, ArCreditHistory, ArInquiry, User#, ArCreditHistoryComment, ArCreditScore, ArScoreFactor, ArResidence, ArPublicRecord, ArEmployer 
from SQL_Aggregate_Strings import QueryData

from Processing_Aggregate_Data import Expand_Methods
from Processing_Merging import Merging_Methods
from Processing_JSON import Flattening_Operations
import pandas as pd

#Class Connection: stores the connection between the user and the server.
class Connection:
    def __init__(self, server, uid, pwd):
        connection_string = ("DRIVER={SQL Server};SERVER=" + server + ";UID=" 
                             + uid + ";PWD=" + pwd)
        connection_string = urllib.quote_plus(connection_string) 
        connection_string = "mssql+pyodbc:///?odbc_connect=%s" % connection_string
        connection = create_engine(connection_string)
        Session = sessionmaker(bind=connection)
        self.session = Session()
    
    #grabs the table defined by SQL Alchey class of name "table" off server
    def grab(self, table):
        return self.session.query(table).all()



# Class Data_Storage: Uses class Connection to initialize with data related
# to the User and ArContact classes.  Stores the methods necessary in order
# to process this data and both convert into JSON, and convert from JSON into
# PANDAS array.

class Data_Storage:
    #requires SQL Server Management Studio credentials on login.
    def __init__(self, server, uid, pwd):

        v = Connection(server, uid, pwd)
        self.Contacts = v.grab(ArContact)
        
        v2 = Connection(server, uid, pwd)
        self.User = v2.grab(User)
        
        self.f = Expand_Methods().formatted_expand_dict
        self.merge = Merging_Methods().group
        self.dat = QueryData()
        self.flattens = Flattening_Operations()
        
        self.str = 0
                
    #Uses method in Expand_Methods() class in order to generate aggregate data
    # for class attributes (eg. averages, maxes and mins) based on strings 
    # specified in QueryData() class, and convert each class into a dictionary
    # of its attributes.
    #
    def aggregate(self):
        for ar_contact in self.Contacts:
            self.f(ar_contact, self.dat.ArContactHandling)

    
    # Returns a list of records contained within new UserPlus classes.
    #    
    # If user is specified merges User attribute with Contacts attribute 
    # (already formatted by the Aggregate method).
    #
    # Either way, each record is placed within a new UserPlus class to contain
    # it.  If comb is 0 or None each independent ArContactId gets their own class.  
    # Else, each UserPlus class contains multiple records for each ArContactId
    # shared by a common Salesforce Id.
    #
    # The resulting list is stored in the .str attribute of this class.
    def Merge(self, user, comb):
        if (user):
            self.str =  self.merge(self.Contacts, self.User, comb)
        else:
            self.str = self.merge(self.Contacts, None, comb)
        

    # Converts each UserPlus class into a dictionary.
    def sort_of_jsonify(self):
        ret = []
        for user in self.str:
            self.f(user, self.dat.User)
            ret.append(user.__dict__)
        self.str = ret

    # Collapses each list/dictionary nested within the current dictionary in list 
    # of dictionaries in .str attribute. _max specifies the maximum amount of 
    # elements that should be returned from any one list the function enocunters.
    def collapse(self, _max):
        ret = []
        for temp in self.str:
            collapsed = self.flattens.diet_flatten_json(temp, self.dat.rmv, mx=_max)
            ret.append(collapsed)
        return pd.DataFrame(ret)
        
    # Does all necessary operations to turn list of SQL Alchemy classes
    # into a list of flat dictionaries.  Largely for testing.
    def full_processing(self, _max):
        self.aggregate()
        self.Merge(None, 0)
        self.sort_of_jsonify()
        self.str = self.collapse(_max)
        return self.str
        
    # common_processing does all processing of data that would be common for 
    # any machine learning query involving this data.
    #
    # unique_processing does processing of data that can be seen as unique for
    # each machine learning query (i.e. the max # of instances of a subclass 
    # extracted from a list of subclasses, )
    # query involving it.
    def common_processing(self, val):
        self.aggregate()
        self.Merge(self.User, val)
        self.sort_of_jsonify()
        
    def unique_processing(self, _max, dep, exc, good_range, filter_vals, no_nulls):
        storage = self.collapse(_max)
        dframe = self.flattens.filter_flattened(storage, dep, filter_vals, no_nulls)
        x, y = self.flattens.flatten_flattened(dframe, dep, exc, good_range)
        return x,y