'''
python dict - to class
copyed from: http://stackoverflow.com/questions/1305532/convert-python-dict-to-object 
Author: Mauro Verzetti
'''
from copy import deepcopy

class struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

    def clone(self, **subs):
        newd = deepcopy(self.__dict__)
        newd.update(subs)
        return struct(**newd)

    def __len__(self):
        return len(self.__dict__)

    def __contains__(self, val):
        return val in self.__dict__

    def __hash__(self):
        return self.__dict__.__repr__().__hash__()

    def __getitem__(self, name):
      'x.__getitem__(i, y) <==> x[i]'
      return self.__dict__[name]

    def __setitem__(self, name, val):
      'x.__setitem__(i, y) <==> x[i]=y'
      self.__dict__[name] = val

    def iteritems(self):
        return self.__dict__.iteritems()

    def keys(self):
        return self.__dict__.keys()

class RecursiveStruct:
    def __init__(self, **entries):
        class_dict = {}
        for key, value in entries.iteritems():
            if isinstance(value, dict):
                class_dict[key] = RecursiveStruct(**value)
            else:
                class_dict[key] = value
        self.__dict__.update(class_dict)

