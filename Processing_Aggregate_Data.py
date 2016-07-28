
import numpy
from scipy.stats import mode

# Expand_Methods(): Contains methods to handle construction of aggregate
# attributes and conversion of lists of classes into lists of dictionaries.
class Expand_Methods():
    
    def __init__(self):
        self.str_l = ["sum", "max", "min", "std", "median", "mean",
                      "variance", "numberofrecords"]
        self.str_s = ["mode", "length"]
        self.str_e = ["exists"]

    # for a numpy array col, returns the sum, max, min, standard 
    # dev., mean, variance, and number of non-zero records for all non NaN 
    # values.
    def zip_up(self, col):
        s = numpy.nansum(col)
        mx = numpy.nanmax(col)
        mn = numpy.nanmin(col)
        std = numpy.nanstd(col)
        md = numpy.nanmedian(col)
        mn_ = numpy.nanmean(col)
        _var = numpy.nanvar(col)
        leng_left = numpy.count_nonzero(~numpy.isnan(col))
        return [s,mx,mn,std, md, mn_, _var, float(leng_left)]
    
    # for a numpy array col, returns the mode,
    # and number of non-zero records for all non NaN values.
    def touch_up(self,col):
        md = mode(col, nan_policy='omit')[0][0]
        leng_left = numpy.count_nonzero(~numpy.isnan(col))
        return [md, float(leng_left)]
    
    # for a numpy array col, returns 1 if non-NaN, non-zero values exist,
    # else returns 0.
    def exists(self,col):
        temp = numpy.nanmax(col)
        _isnan = numpy.isnan(temp)
        return [numpy.nanmax(col) and 1.0 - _isnan]
    

    # for each attribute [attr] for each class instance in 
    # [parent_object].[attribute_to_expand]:
    #      
    #   if [attr] in exists_names: runs exists over [attr] fields for all 
    #   classes and adds a field to parent_object with value 
    #   1 if data exists for that value on some record, else 0.
    #
    #   elif [attr] in converted_string_names:
    #       runs touch_up over [attr] fields for all classes and adds
    #       fields to the parent object with the mode of records and the
    #       number of records.
    #
    #   elif [attr] in avoid_names: does nothing
    #
    #   else: runs zip_up() over [attr] fields for all classes and adds
    #   relevant fields to the parent_object.
    #
    #  Finally: checks exists_names.  If non-empty, then adds a single
    #  field [parent_object].[_aggr_name_] with value 1 if data exists
    #  on some record for at least one of the fields in exists_names
    #  or 0 if data does not exist for any of the records for any of 
    #  the fields. 
    def expand_dict_all(self, parent_object, attribute_to_expand, exists_names, 
                        converted_string_names, avoid_names, exists_multi, 
                        _aggr_name_):

        if (attribute_to_expand == ""):
            return
        
        location = parent_object.__dict__[attribute_to_expand]
        leng_left = len(location)
        if (leng_left) == 0:
            return
        
        fields = [a for a in location[0].__dict__.keys() if (a[0] != '_')]
        for val in fields:
            if not (val in avoid_names):
                pre_list = [obj.__dict__.get(val) for obj in location]
                processing_list = numpy.array([a for a in pre_list if a != None])
                processed = []
                if (val in converted_string_names):
                    processed = self.touch_up(processing_list)
                    _string = self.str_s
                elif (val in exists_names):
                    processed = self.exists(processing_list)
                    _string = self.str_e
                else:
                    processed = self.zip_up(processing_list)
                    _string = self.str_l
                for i in range(len(processed)):
                    parent_object.__dict__[val + '_^_' + _string[i]] = processed[i]

        parent_object.__dict__[attribute_to_expand + '_^_' 'leng_left'] = leng_left
    
        if (exists_multi):
            value = 0
            for val in exists_multi:
                col = numpy.array([obj.__dict__[val] for obj in location])
                value = value + self.exists(col)[0]
            parent_object.__dict__[_aggr_name_] = value and 1.0
        
        return
    
    
    # For each class contained within the list of classes in [parent_obj].[subq
    # replace it with a dictionary.s
    def replace(self, parent_object, subq):
        original_l = parent_object.__dict__[subq]
        _acc = []
        for original in original_l:
            original_dict = original.__dict__
            modified = {k:v for k,v in original_dict.iteritems() if k[0] != '_'}
            _acc.append(modified)
        parent_object.__dict__[subq] = _acc
        return


    # Processes strings containing data on construction of
    # aggregate attributes and how lists of subclasses should
    # be handled.  See SQL_Aggregate_Strings.py for documentation
    # on how these strings should be formatted.
    def formatted_expand_dict(self, parent_object, string):
       
        _calls = string.split('\n')
       
        for call in _calls:
            attribute_to_expand = ""
            _aggr_name_ = ""
            exists_multi = []
            converted_string_names = []
            avoid_names = []
            exists_names = []
            subqs = []
            subqs_rmv = []
            conv_flag = 0

            _variables = call.split('|')

            for term in _variables:
                terms = term.split(' ')  
                if (terms[0] == "ATTR"):
                    attribute_to_expand = terms[1]
                    if (len(terms) > 2):
                        conv_flag = 1
                elif (terms[0] == "STR"):
                    converted_string_names = terms[1:]
                elif (terms[0] == "AVD"):
                    avoid_names = terms[1:]
                elif (terms[0] == "EXISTS"):
                    exists_names = terms[1:]
                elif (terms[0] == "SUBQ"):
                    subqs = terms[1:]
                elif (terms[0] == "SUBQRMV"):
                    subqs_rmv = terms[1:]
                elif (terms[0] == "EXISTSM"):
                    _aggr_name_ = terms[1]
                    exists_multi = terms[2:]

            if (attribute_to_expand == "__self__"):
                for subq in subqs:
                    self.replace(parent_object, subq)
                for subq in subqs_rmv:
                    del parent_object.__dict__[subq]
                    
            else:
          
                self.expand_dict_all(parent_object, attribute_to_expand, 
                                     exists_names, converted_string_names, 
                                     avoid_names, exists_multi, _aggr_name_)
                if (conv_flag):
                    object_loc = parent_object.__dict__[attribute_to_expand]
                    for i in object_loc:
                        for subq in subqs:
                            self.replace(i, subq)
                        for subq in subqs_rmv:
                            del i.__dict__[subq]
        return 