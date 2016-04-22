from syn.five import STR

def join(obj, sep=' '):
    if isinstance(obj, list):
        return sep.join(obj)
    return obj

def split(obj, sep=None):
    if isinstance(obj, STR):
        if sep is None:
            return obj.split()
        return obj.split(sep)
    return obj

def dictify_strings(obj, empty=True, sep=None):
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
