from syn.five import STR

#-------------------------------------------------------------------------------
# Argument processors

def join(obj=None, sep=' '):
    if isinstance(obj, list):
        return sep.join(obj)
    return obj

def split(obj=None, sep=None):
    if isinstance(obj, STR):
        if sep is None:
            return obj.split()
        return obj.split(sep)
    return obj

def dictify_strings(obj=None, empty=True, sep=None):
    if isinstance(obj, list):
        ret = {}
        for s in obj:
            if empty:
                name = s
                val = ''
            else:
                name, val = s.split(sep)
            ret[name.strip()] = val.strip()
        return ret
    return obj

#-------------------------------------------------------------------------------
# __all__

__all__ = ('join', 'split', 'dictify_strings')

#-------------------------------------------------------------------------------
