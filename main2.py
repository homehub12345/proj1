import numpy
from Main_Machine_Learning_2 import Machine_Learning_Methods
from Main_Extraction import Data_Storage
from SQL_Types import force
#import Machine_Learning_Methods from Main_Machine_Learning_2
#import Data_Storage from Main_Extraction


class Main():
    def __init__(self, serv, us, pw, merge_val):
		self.D_St = Data_Storage(serv, us, pw)
		self.D_St.common_processing(merge_val)
		self.M_L = Machine_Learning_Methods()
		self.max = 8
		self.exc = []
		self.no_nulls = 1

    def change_processing_pars(self, max_depth, fields_to_exclude, no_nulls):
         self.max = max_depth
         self.exc = fields_to_exclude
         self.no_nulls = no_nulls

    #load_xy: loads data off data storage object and onto x and y values
    #data storage object persists to allow for multiple calls without requiring
    #reloading data off the SQL server.
    #
    # _dep: name of the dependent variable
    #
    # good_range: range in which the dependent variable is changed into label "good" 
    # any value not in this class becomes categorized into label "bad"  
    def load_xy(self, _dep, good_range, filter_vals = []):

        self.M_L.x, self.M_L.y = (self.D_St).unique_processing(self.max, _dep, 
        														 self.exc, 
                                                         		 good_range, 
                                                         		 filter_vals, 
                                                         		 self.no_nulls)
        self.M_L.y = numpy.ravel(self.M_L.y)



    #Runs load_xy with predetermined parameters
    #parameters determined based on the string "mode".
    def auto_xy(self, mode):

        if (mode == "late"):
            strg = self.exc = "OperationStatusId"
            self.load_xy("records_0_late", [0, 0.0])
            self.exc = strg

        #elif (mode == "late mortgage"):

        #    valid_mortgages = ['ConventionalRealEstateMortgage', 
        #                       'FarmersHomeAdministration',
        #                       'FHARealEstateMortgage',
        #                       'HomeEquityLineofCredit',
        #                       'RealEstateMortgageWithoutOtherCollateral',
        #                       'ResidentialLoan',
        #                       'VeteransAdministrationRealEstateMortgage']

        #    filter_vals = [force(str) for str in valid_mortgages]
            
        #    storage = self.D_St.collapse(self.max)
        #    dframe = self.D_St.flattens.filter_flattened(storage, "LoanType", 
        #                                                 filter_vals, 
        #                                                 self.no_nulls)

        #    dframe = self.D_St.flattens.filter_flattened(storage, 
        #                                                 "records_0_late", 
        #                                                 [], 
        #                                                 self.no_nulls)

        #    self.M_L.x, self.M_L.y = (self.D_St).flattens.filter_flattened (
        #                              dframe, "records_0_late", "OperationStatusId", 
        #                             [0,0.0]
        #                              )

            self.M_L.y = numpy.ravel(self.M_L.y)

        elif (mode == "o_id"):
            exc_lst = [213, 215, 216, 217, 218, 221, 223, 224, 225, 226, 233, 
                       236, 237, 261]
            good_lst = [231]
            self.load_xy("OperationStatusId", good_lst, exc_lst)
        elif (mode == "o_id biased good"):
            exc_lst = [213, 215, 216, 217, 218, 221, 223, 226, 233, 236, 237, 
                       261]
            good_lst = [224, 225, 231]
            self.load_xy("OperationStatusId", good_lst, exc_lst)
        elif (mode == "o_id biased bad"):
            exc_lst = [213, 215, 216, 217, 218, 221, 223, 226, 233, 236, 237, 
                       261]
            good_lst = [231]
            self.load_xy("OperationStatusId", good_lst, exc_lst)
        else:
            print "bad mode"
            print "implemented modes include:"
            print "[late, o_id, o_id biased good, o_id biased bad, late mortgage]"  

    def update_model(self, new_model):
        self.M_L.cur_model = new_model
        return 0
        
    # runs machine_learning method specified by [operation] and loads
    # data into file specified by [output_to], with parameters loaded
    # by self.auto.xy([mode])
    def run_machine_learning(self, mode, operation, output_to = ""):
        self.auto_xy(mode)
        if (operation == "feature_importance"):
            self.M_L.feature_importance(self.M_L.cur_model, output_to)
        elif (operation == "run_model"):
            self.M_L.run_model(self.M_L.cur_model, output_to)
        else:
            print("not supported at this time.")
            return 0

#    def drunk_machine_learning(self, mode, operation, output_to=""):
 #   		return self.drunk_machine_learning(mode, operation, output_to)
