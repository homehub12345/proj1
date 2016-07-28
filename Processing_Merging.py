
import numpy

#Class UserPlus:
#   consists of a user with their OperationStatusId, SalesforceId,
#   and relevant records.
class UserPlus():
	def __init__(self, o_id, s_id, _rest):
		self.OperationStatusId = o_id
		self.SalesforceContactId = s_id
		self.records = _rest
    

class Merging_Methods():
	#partial src: http://stackoverflow.com/questions/5695208/group-list-by-values

    # Returns tuple (0.0, numpy.nan) if x is None type, else, returns its 
    # SalesforceContactId and OperationStatusId
    #
    def mapper(self, x):
        if x == None:
            return (0.0,numpy.nan)
        else:
            return (x.SalesforceContactId, x.OperationStatusId)
            
    # Transforms the ar_lst and us_lst (if specified) into a list of UserPlus 
    # classes
    #
    # If us_lst NOT specified: loads 0.0 as a placeholder OperationStatusId
    # else: loads OperationStatusId corresponding with the given SalesforceId
    #
    # If _solo: each User_Plus contains all ArContactIds for a SalesforceId
    # else: each User_Plus contains only 1 ArContactId

    # UserPlus() classes arranged by type.
    def group(self, ar_lst, us_lst, _solo):
        new_list = []
        if (us_lst):
	        v = list(set([self.mapper(x) for x in us_lst]))
               #(set(map(lambda x:(x.SalesforceContactId, x.OperationStatusId), us_lst)))
	        if (_solo):
	            new_list = [UserPlus(z[1], z[0], [y for y in ar_lst if y.SalesforceContactId == z[0]]) for z in v]
	            #x = 0
	        else:
                 conv = {a[0]:a[1] for a in v}
                 new_list = [UserPlus(conv.get(y.SalesforceContactId, numpy.nan), y.SalesforceContactId, [y]) for y in ar_lst]
        else:
	        v = list(set(map(lambda x:x.SalesforceContactId, ar_lst)))
	        if (_solo):
	            new_list = [UserPlus(0.0, x, [y for y in ar_lst if y.SalesforceContactId == x]) for x in v]
	        else:
	            new_list = [UserPlus(0.0, y.SalesforceContactId, [y]) for y in ar_lst]
        return new_list

