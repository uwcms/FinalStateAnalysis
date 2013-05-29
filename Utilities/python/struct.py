'''
python dict - to class
copyed from: http://stackoverflow.com/questions/1305532/convert-python-dict-to-object 
'''
class struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)
