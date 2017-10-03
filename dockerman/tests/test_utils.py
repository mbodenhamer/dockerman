import dockerman.utils as du

#-------------------------------------------------------------------------------
# Argument processors

def test_join():
    assert du.join() == None
    assert du.join(['a', 'b']) == 'a b'
    assert du.join(['a', 'b'], ',') == 'a,b'

def test_split():
    assert du.split() == None
    assert du.split('a b') == ['a', 'b']
    assert du.split('a,b') == ['a,b']
    assert du.split('a,b', ',') == ['a', 'b']

def test_dictify_strings():
    assert du.dictify_strings() == None
    assert du.dictify_strings(['a=b', 'c=d']) == {'a=b': '', 'c=d': ''}
    assert du.dictify_strings(['a = b', 'c = d'], sep='=') == \
        {'a = b': '', 'c = d': ''}
    assert du.dictify_strings(['a = b', 'c = d'], sep='=', empty=False) == \
        dict(a='b', c='d')

#-------------------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    from syn.base_utils import run_all_tests
    run_all_tests(globals(), verbose=True, print_errors=False)
