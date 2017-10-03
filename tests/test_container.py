from dockerman import Container

#-------------------------------------------------------------------------------
# Container creation/deletion

def test_container_create_delete():
    #c = Container('mbodenhamer/alpine-data', detach=True)
    pass

#-------------------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    from syn.base_utils import run_all_tests
    run_all_tests(globals(), verbose=True, print_errors=False)
