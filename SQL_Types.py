#new type conversion runs directly from SQL Alchemy


from sqlalchemy import Column, Integer, Sequence, types, Float, func, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import cast
import numpy as np
import datetime

st_date = datetime.date(1900,1,01)

# function converts _str to float
# for concerns over time complexity, a simple method has
# been posted below, with a more complicated method commented out.
def force(_str):
	if(_str):
         return len(_str) + 100 * (ord(_str[0])) + 10000 * (ord(_str[-1]))
		#it_ = 0
		#div_ = 90.0
		#acc_ = 0.0
		#const_ = ord(' ')
		#for i in _str:
		#	it_ = it_ + 1.0
		#	if (it_ < 4):
		#		acc_ = acc_ + float(ord(i))/div_
		#		div_ = div_ * div_
		#	else:
		#		acc_ = acc_ + float(ord(i))
		#return acc_
	else:
		return 0.0
  

# function converts _str representing date into a float representing
# the seconds since that date and January 1st 1900.
def str_to_day(_str):
    l = [int(a) for a in _str.split('-')]
    z = datetime.date(l[0],l[1],l[2]) - st_date
    return float(z.days)


#collation class, based on:
#http://stackoverflow.com/questions/2680140/case-insensitive-string-columns-in-sqlalchemy

#Class converts strings to floats.
class S_String(types.TypeDecorator):
    impl = types.String
    def process_bind_param(self, value, dialect):
        return value
    def process_result_value(self, value, dialect):
        if (value == None):
            return 0.0
        else:
            return force(value)
        #    return force(value)

#Class converts int to float (converts Nones to Zeroes)
class S_Int_z(types.TypeDecorator):
    impl = types.String
    def process_bind_param(self, value, dialect):
        return value
    def process_result_value(self, value, dialect):
        if (value == None):
            return 0.0
        else:
            return float(value)

#Class converts int to float (converts Nones into numpy.NaN, which will
#   later be replaced by average values for an attribute)
class S_Int_a(types.TypeDecorator):
    impl = types.String
    def process_bind_param(self, value, dialect):
        return value
    def process_result_value(self, value, dialect):
        if (value == None):
            return np.nan
        else:
            return float(value)

#converts date to float (converts Nones to Zeroes)
class S_Date_z(types.TypeDecorator):
    impl = types.DateTime
    def process_bind_param(self, value, dialect):
        return value
    def process_result_value(self, value, dialect):
        if (value == None):
            return 0.0
        else:
            t_diff = value - st_date
            d = t_diff.days
            return float(d)

#converts int to float (converts Nones into numpy.NaN, which will
#   later be replaced by average values for an attribute).
class S_Date_a(types.TypeDecorator):
    impl = types.DateTime
    def process_bind_param(self, value, dialect):
        return value
    def process_result_value(self, value, dialect):
        if (value == None):
            return np.nan
        else:
            return value
      
#converts Date string to float (with 0s)
class S_SDate_z(types.TypeDecorator):
    impl = types.String
    def process_bind_param(self, value, dialect):
        return value
    def process_result_value(self, value, dialect):
        if (value == None):
            return 0.0
        else:
            return str_to_day(value)

#converts Date string to float (converts Nones into numpy.NaN, which will
#   later be replaced by average values for an attribute).
class S_SDate_a(types.TypeDecorator):
    impl = types.String
    def process_bind_param(self, value, dialect):
        return value
    def process_result_value(self, value, dialect):
        if (value == None):
            return np.nan
        else:
            return str_to_day(value)


