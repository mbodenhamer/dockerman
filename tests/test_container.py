from dockerman import Container

#-------------------------------------------------------------------------------
# run args marshalling

def test_container_marshal_run_args():
    c = Container('ubuntu')
    assert c.marshal_args() == ' ubuntu'

    c = Container('debian:jessie', 'python foo.py',
                  tty=True, stdin_open=True, name='test',
                  volumes_from=['foo', 'bar'])
    assert c.marshal_args() == (' -t -i --volumes-from foo --volumes-from bar '
                                '--name test debian:jessie python foo.py')

#-------------------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    from syn.base_utils import run_all_tests
    run_all_tests(globals(), verbose=True, print_errors=False)
