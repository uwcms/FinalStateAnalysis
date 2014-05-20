class SmartDict(object):
    '''Smart dictionary for storing objects. Book an object key with book method, 
    call it like with a dictionary. But the object is created ONLY when called the first time, 
    if it never gets called it never gets created, saving memory and time'''
    def __init__(self, *args, **kargs):
        self.active = {} #active keys
        self.booked = {} #booked (not yet active) keys

    def book(self, key, type, *args, **kwargs):
        self.booked[key] = (type, args, kwargs)

    def keys(self):
        return self.active.keys()+self.booked.keys()

    def items(self):
        booked = self.booked.keys()
        for key in booked:
            self.__activate__(key)

        return self.active.items()

    def values(self):
        booked = self.booked.keys()
        for key in booked:
            self.__activate__(key)

        return self.active.values()

    def __activate__(self, key):
        kind, args, kwargs = self.booked[key]
        if len(args) and len(kwargs):
            self.active[key] = kind(*args, **kwargs)
        elif len(args): #and not kwargs
            self.active[key] = kind(*args)
        elif len(kwargs): #and not args
            self.active[key] = kind(**kwargs)
        del self.booked[key]
        return None
    
    def __getitem__(self, key):
        if key in self.active:
            return self.active[key]
        elif key in self.booked:
            self.__activate__(key)
            return self.active[key]
        else:
            raise KeyError("%s" % key.__repr__())
