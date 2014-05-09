""" Converts any Python object to dictionary recursively
    including iterating over iterables
"""
def todict(obj):
    """ Converts object to dictionary recursively
        (Object, str) -> {str : object}
    """
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v)
        return data
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__"):
        return [todict(v) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value)) 
            for key, value in obj.__dict__.iteritems() 
            if not callable(value) and not key.startswith('_')])
        return data
    else:
        return obj