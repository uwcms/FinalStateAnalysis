'''
only a couple of json functions made prettier
'''
import json

def dumps(obj, indent = 4, separators = (',', ': '), **kwargs):
    return json.dumps(obj, indent=indent, separators=separators, **kwargs)

def convert(input):
    '''converts json unicode strings into bytecode strings'''
    if isinstance(input, dict):
        return dict([(convert(key), convert(value)) for key, value in input.iteritems()])
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input  


def loads( input, object_hook=convert, **kwargs):
    return json.loads( input, object_hook=object_hook, **kwargs )
