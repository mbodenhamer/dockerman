from dockerman.cmdargs import (arglist, Argument, Positional, Option, 
                               BinaryOption, render_args)

#-------------------------------------------------------------------------------
# Positional

def test_positional():
    arg1 = Positional('arg1')
    arg2 = Positional('arg2', repeatable=True, quote='never')
    arg3 = Positional('arg3', quote_elements=True)

    assert arg1.render(3) == '3'
    assert arg1.render([1, 2]) == '"1 2"'

    assert arg2.render('abc') == 'abc'
    assert arg2.render(['abc', 'def']) == 'abc def'

    assert arg3.render(['a', 'b', 'c']) == '"a" "b" "c"'

#-------------------------------------------------------------------------------
# Option

def test_option():
    opt1 = Option('-b', ('--b-option', '--b-alias'))
    opt2 = Option('-c', interleave=False)
    opt3 = Option('--foo', use_eq=True)

    assert opt1.name == '-b'
    assert opt1.aliases == ['--b-option', '--b-alias']
    
    assert opt1.render(3) == '-b 3'
    assert opt1.render([1, 2]) == '-b 1 -b 2'
    
    assert opt2.render(3) == '-c 3'
    assert opt2.render([1, 2]) == '-c "1 2"'

    assert opt3.render(3) == '--foo=3'
    assert opt3.render([1, 2]) == '--foo=1 --foo=2'

#-------------------------------------------------------------------------------
# BinaryOption

def test_binaryoption():
    arg1 = BinaryOption('-b')
    assert arg1.render(True) == '-b'
    assert arg1.render(False) == ''

#-------------------------------------------------------------------------------
# arglist

def test_arglist():
    args = []
    with arglist(args):
        arg1 = Positional('arg1')
        arg2 = Positional('arg2')
        arg3 = Positional('arg3')
        arg4 = BinaryOption('-b')

    assert args == [arg1, arg2, arg3, arg4]
    assert Argument._arglist is None
    assert Argument._arglist is Positional._arglist
    assert Argument._arglist is BinaryOption._arglist

    args = []
    with arglist(args):
        argd = dict(arg1 = Positional('arg1'),
                    arg2 = Positional('arg2'),
                    arg3 = Positional('arg3'),
                    arg4 = BinaryOption('arg4'))

    assert args == [argd['arg1'], argd['arg2'], argd['arg3'], argd['arg4']]

#-------------------------------------------------------------------------------
# render_args

def test_render_args():
    args = []
    with arglist(args):
        BinaryOption('-a')
        Option('-b')
        BinaryOption('-d')
        Positional('c')
        
    values = {'-a': True,
              '-b': [1, 2],
              'c':  'abc',
              '-d': False}

    assert render_args(args, values) == ' -a -b 1 -b 2 abc'

#-------------------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    from syn.base_utils import run_all_tests
    run_all_tests(globals(), verbose=True, print_errors=False)
