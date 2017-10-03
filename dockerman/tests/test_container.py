from nose.tools import assert_raises
from dockerman import Container, ContainerStatus, RA, CC
from syn.base_utils import assign

#-------------------------------------------------------------------------------
# Status

def test_containerstatus():
    s = ContainerStatus()

    assert s.id is None
    assert s.ip_addr is None
    assert s.exists is False
    assert s.running is False
    assert s.paused is False
    assert s.dict == {}

    s.id = 'abc'
    s.exists = True
    s.dict = dict(a=1)

    assert s.id == 'abc'
    assert s.exists is True
    assert s.dict == dict(a=1)

    s.reset()
    assert s.id is None
    assert s.ip_addr is None
    assert s.exists is False
    assert s.running is False
    assert s.paused is False
    assert s.dict == {}

#-------------------------------------------------------------------------------
# Container

def test_container():
    c = Container('foo')
    assert c.image == 'foo'
    assert hasattr(c, 'name')
    assert c.status == ContainerStatus()

    def bad(con):
        con.status = 'xyz'

    def bad2(con):
        del con.status

    assert_raises(AttributeError, bad, c)
    assert_raises(AttributeError, bad2, c)

#-------------------------------------------------------------------------------
# run args marshalling

def test_container_marshal_run_args():
    Container
    c = Container('ubuntu')

    with assign(c, 'name', None):
        assert c.marshal_args(RA) == ' ubuntu'
        assert c.marshal_args(CC) == dict(tty = False,
                                          image = 'ubuntu',
                                          stdin_open = False,
                                          host_config = {},
                                          network_disabled = False,
                                          detach = False)

    with assign(c, 'name', None):
        c = Container('debian:jessie', 'python foo.py',
                      tty=True, stdin_open=True, name='test',
                      volumes_from=['foo', 'bar'])
        assert c.marshal_args(RA) == (' -t -i --volumes-from foo --volumes-from bar '
                                      '--name test debian:jessie python foo.py')

    assert_raises(ValueError, c.marshal_args, 'foo')

#-------------------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    from syn.base_utils import run_all_tests
    run_all_tests(globals(), verbose=True, print_errors=False)
