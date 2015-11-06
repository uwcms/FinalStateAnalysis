'''
python dict - to class
copyed from: http://stackoverflow.com/questions/1305532/convert-python-dict-to-object 
'''
from copy import deepcopy
class struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)
    def clone(self, **subs):
        newd = deepcopy(self.__dict__)
        newd.update(subs)
        return struct(**newd)
class RecursiveStruct:
    def __init__(self, **entries):
        class_dict = {}
        for key, value in entries.iteritems():
            if isinstance(value, dict):
                class_dict[key] = RecursiveStruct(**value)
            else:
                class_dict[key] = value
        self.__dict__.update(class_dict)
