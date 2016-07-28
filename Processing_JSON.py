import numpy
from scipy.stats import mode
import pandas as pd
from sklearn.preprocessing import Imputer




# class flattening_operations(): contains methods to flatten a dictionary of
# dictionaries and convert it into a PANDAS array. 
# 
class Flattening_Operations():
    
    def __init__(self):
        self.imp = Imputer(missing_values='NaN', strategy="mean", axis=0)
    
    #Flattens dictionary of dictionaries y and converts to pandas array.  
    #Converts both nested lists and dictionaries into elements of 
    #the top-level dictionary.
    #
    # If mx is set to an int that is not None, at most mx elements from
    # any list will have their elements inserted into the top level array.
    # The rest will be removed.
    #
    # If a key is encountered in a dictionary that is contained within the
    # list exempt, it will not be placed into the top-level dictionary and
    # instead be removed. 
    def diet_flatten_json(self, y, exempt, mx = None):
        out = {}
        def flatten(x, name=''):
            
            if type(x) is dict:
                for a in x:
                    if (not (a in exempt)):
                        flatten(x[a], name + a + '_')
            
            elif type(x) is list:
                _length = len(x)
                i = 0
                j = 0
                for i in range(min([mx, _length]) or _length):
                    flatten(x[i], name + str(i) + '_')
                if ((i < (mx - 1) or _length-1) and (i > 0)):
                   # print(mx)
                   # print(_length)
                   # print("I IS")
                   # print(i)
                    for j in range(i, mx):
                   #     print("FLATTENING NOW")
                        flatten(x[i], name + str(j) + '_')                        

            else:
                out[name[:-1]] = x
        flatten(y)
        return out
    

    #not currently in use, but planned for future implementation
    #will eventually be used to deal with lists for which more
    #records exist for one class than do for others, to ensure missing
    #dictionaries in a list of dictionaries are replaced with a dictionary
    #containing the average across all dictionaries. 
    def flat_and_out(self, dict_list_range):
        dataframe = pd.dataframe(dict_list_range).values
        means = dataframe.mean()
        return means.to_dict()
    
    # Maps values to "Unknown" if v is of type numpy.NaN,
    # "Good" if v is contained within list good_range,
    # and "Bad" otherwise.
    # Used for labeling the dependent variable.    
    def unary_mapper(self, v, good_range):
        if (v != v):
            return "Unknown"      
        elif (v in good_range):
            return "Good"
        else:
            return "Bad"
            
    # Takes x as input.  If [no_nulls] is specified as a value that does
    # not evaluate to False, simply returns True if x is not in list of
    # values to be filtered out [filter_vals], else False.  If [no_nulls]
    # specified, then False will additionally be returned if x is a numpy.NaN,
    # regardless of whether or not it is in the list. 
    def filter_x(self, x, filter_vals, no_nulls):
        t1 = True
        if (no_nulls):
            t1 = not(numpy.isnan(x))
        t2 = x not in filter_vals
        return t1 and t2
    
    # Filters out all rows in PANDAS array flattened for which the dependent
    # variable falls within filter_vals (and if no_nulls specified, all rows for
    # which the dependent variable evalutes to a numpy.nan)
    def filter_flattened(self, flattened, dependent, filter_vals, no_nulls):
        df = pd.DataFrame(flattened)
        rows = df[dependent].map(lambda x: self.filter_x(
                                    x, filter_vals, no_nulls
                                 ))        
        return df[rows]
        
    # From dataframe df, removes all columns in exc, removes all entirely nan
    # columns, transforms the dependent variable column into "Good", "Bad", 
    # and "Unknown"s when the variable is in good_range, not in good_range,
    #  or a numpy.nan  (respectively), and replaces numpy.nan data with the
    #  means for the columns in which they are contained.
    #
    # returns independant, and dependant as a tuple.
    def flatten_flattened(self, df, dependent, exc, good_range):

        f_x =  df[dependent]
        nans = df.isnull().all()
        non_false = [c for c, _isnan in zip(df.columns, nans) if not (_isnan)]
        df = df[non_false]

        col_names = [c for c in df.columns if (c != dependent) 
                     and not (c in exc)]
        #print(col_names)
        x = df[col_names]
        independant = pd.DataFrame(self.imp.fit_transform(x), columns = col_names)
        dependant = pd.DataFrame([self.unary_mapper(c, good_range) for c in f_x], 
                               columns=["Dependent"])
        return (independant, dependant)
    
    # deprecated; src code for flattening a dictionary from StackExchange
    def flatten_json(y):
        out = {}
        def flatten(x, name = ''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x
        flatten(y)
        return out