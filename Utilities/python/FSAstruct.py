'''
python dict - to class
copyed from: http://stackoverflow.com/questions/1305532/convert-python-dict-to-object 
'''
class FSAstruct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

class RecursiveStruct:
    def __init__(self, **entries):
        class_dict = {}
        for key, value in entries.iteritems():
            if isinstance(value, dict):
                class_dict[key] = RecursiveStruct(**value)
            else:
                class_dict[key] = value
        self.__dict__.update(class_dict)
