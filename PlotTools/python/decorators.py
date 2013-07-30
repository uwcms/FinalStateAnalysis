from functools import update_wrapper

def decorator(d):
    "Make function d a decorator that wraps function fn"
    return lambda fn: update_wrapper(d(fn),fn)

decorator = decorator(decorator)

@decorator
def memo(fn):
    "Decorato to memoize (cache) results of a function"
    cache = {}
    def _f(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        try: #check if we have it in cache
            return cache[key]
        except KeyError: #No, we don't
            cache[key] = result = fn(*args, **kwargs)
            return result
        except TypeError: #Actually, the args cannot even be a key of dict (like lists)
                          #print "this cannot be cached: %s" % type(args)
            return fn(*args, **kwargs)
    return _f

@decorator
def memo_last(fn):
    '''Decorato to memoize (cache) the last results of a function, 
    this helps caching event-based functions, slow to compute that 
    are called more than once per event, but events never repeat'''
    cache = {}
    def _f(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        try: #check if we have it in cache
            return cache[key]
        except KeyError: #No, we don't
            cache.clear()
            cache[key] = result = fn(*args, **kwargs)
            return result
        except TypeError: #Actually, the args cannot even be a key of dict (like lists)
                          #print "this cannot be cached: %s" % type(args)
            print "cannot do"
            return fn(*args, **kwargs)
    return _f
        
