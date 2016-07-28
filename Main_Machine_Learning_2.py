# File contains methods for machine learning and relevant data.

import numpy
from Main_Extraction import Data_Storage
from sklearn.ensemble import ExtraTreesClassifier

# Class contains methods for machine learning and relevant data
class Machine_Learning_Methods():
    
    #initializes the function
    def __init__(self):		
        self.feature_model = ExtraTreesClassifier(max_features = 300, n_estimators = 650, criterion = "gini", warm_start=False, n_jobs = 4)
        self.operation_model = ExtraTreesClassifier(max_features = 300, n_estimators = 650, criterion = "gini", warm_start=False, n_jobs = 4)
        self.late_model = ExtraTreesClassifier(max_features = 300, n_estimators = 3000, min_samples_split = 2000, criterion = "gini", warm_start=False, n_jobs = 4)
        self.cur_model = self.operation_model
        #self.server = serv
        #self.user = us
        #self.password = pw
        self.st_obj = 0
        self.x = 0
        self.y = 0
        #self.max = 8
        #self.exc = []
        #self.no_nulls = 1
        
    #sets the parameters for logging in to the relevant server     
    # server is server, us is user, pw is password
	def change_obj_pars(self, serv, us, pw):
         self.server = serv
         self.user = us
         self.password = pw
     
    #sets the parameters for processing the data storage object in which the
    #SQL Alchemy JSON is contained within.
    #
    # max_depth: maximum # of records taken from each subquery/list of subclasses.  
    # fields_to_exclude: fields in the SQL Alchemy JSON that will be entirely 
    # removed if encountered by script.
    # no_nulls: If set to 1, then the scipt automatically filters out data for
    # which the dependent field is missing data.
     
    def change_processing_pars(self, max_depth, fields_to_exclude, no_nulls):
        self.max = max_depth
        self.exc = fields_to_exclude
        self.no_nulls = no_nulls
    
    
    # loads object off sql alchemy server and onto data storage object
    # serv: server; us: username; pw: password; merge_val: if 1 data storage
    # object contains list of collections of users, if 0, data storage object
    # contains list of users.
    def load_obj(self, merge_val=0):
        self.st_obj = Data_Storage(self.serv, self.us, self.pw)
        self.st_obj.common_processing(merge_val)

    
    # evaluates mearching learning using run_model function with self.cur_model
    def auto_eval(self, mode, output_name=""):
        self.auto_xy(mode)
        self.run_model(self.cur_model, output_name)
    
    #Evaluates machine learning model "model" using sk-learn's built in cross
    # validation
    def evaluate_learning(self, model):
        from sklearn import cross_validation
        print("Preparing for Cross-Validation!")
        scores = cross_validation.cross_val_score(model, self.x, 
            self.y, cv = 3)
        print("Accuracy: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))


    # helper function for run_model to get correct index ranges
    def split_ind(self, ind, i):
        rel = [j for j in range(len(ind)) if j != i]
        cum = []
        for k in rel:
            cum = cum + [j for j in ind[k]]
        return (cum, ind[i])


    #Evaluates machine learning "model" using custom cross-validation.  
    # outputs total accuracy rate across all data, false positive rate,
    # and false negative rate.
    #
    # If output_to specified, then writes this info to a file.
    def run_model(self, model, output_to=None):
        sz = len(self.x)
        indices = numpy.random.permutation(range(sz))
        new_sz = round(sz * float(1) / float(5))
        sizes = [int(new_sz*i) for i in range(6)]
        ind = [indices[sizes[j]:sizes[j + 1]] for j in range(5)]
        y_v = self.y
        x_v = self.x.values
        f_p = []
        f_n = []
        tot_n = []
        tot_p = []

        for i in range(len(ind)):
            print("On run %0.4f", i)
            _test, _train = self.split_ind(ind, i)
            model.fit(x_v[_train], y_v[_train])
            test = model.predict(x_v[_test])
            accuracy = [((z1 == z2), z1, z2) for z1,z2 in zip(test,y_v[_test])]
            
            f_p = f_p + [a[0] for a in accuracy if (a[0] == False) and (a[1] == "Good")]
            tot_n = tot_n + [a[2] for a in accuracy if (a[2] == "Bad")]
            f_n = f_n + [a[0] for a in accuracy if (a[0] == False) and (a[1] == "Bad")]
            tot_p = tot_p + [a[2] for a in accuracy if (a[2] == "Good")]
            print(len(tot_p), len(tot_n), len(f_p), len(f_n))
                    
        fpr = len(f_p)/float(len(tot_n))   
        fnr = len(f_n)/float(len(tot_p))
        tar = float(len(tot_n) + len(tot_p) - len(f_p) - len(f_n))/float(len(tot_n) + len(tot_p))           

        print("Done.  Loading data.")
        print("Returning Data")
        print("Overall Accuracy: %0.4f.  False Positive Rate: %0.4f."  
        "False Negative Rate: %0.4f.",
        tar, fpr, fnr)
            
        if (output_to):
            f = open(output_to, "w")
            f.write(("5-Fold Cross Validation Results\n"
                    "\t Average Accuracy On All: " + str(tar) + " \n"
                    "\t False Positive Rate: " + str(fpr) + "\n"
                    "\t False Negative Rate: " + str(fnr) + "\n")
                    )
            f.close()

    # orders features analyzed by machine learning method "model" by importance
    def feature_importance(self, model, output_to=""):
        #x, y = self.st_obj.unique_processing(_max, dep, exc)
        model.fit(self.x,self.y)
        feat = [(c,b) for c,b in zip(self.x.columns, model.feature_importances_)]
        sort = sorted([(w, v) for v,w in feat], reverse = True)
        if (output_to):
            f = open(output_to, "w")
            f.write(str(sort))
            f.close()
        return sort
    
    #TODO: will learn from the storage object and predict on an inputted data 
    #set
    def learn_predict(self, st_obj, dep, exc, model):
        print("TODO")
        return 0
     