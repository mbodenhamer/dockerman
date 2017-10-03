from dockerman import Container, container
from dockerman.utils import call, container_exists

#-------------------------------------------------------------------------------
# Container start/stop/etc.

def test_container_start_stop():
    c = Container('mbodenhamer/alpine-data', detach=True)
    assert c.status.exists is False
    
    c.run()
    assert c.status.exists is True
    assert c.status.running is True
    assert c.status.paused is False

    assert container_exists(c.name)

    c.pause()
    assert c.status.exists is True
    assert c.status.running is True
    assert c.status.paused is True

    c.unpause()
    assert c.status.exists is True
    assert c.status.running is True
    assert c.status.paused is False

    c.stop()
    assert c.status.exists is True
    assert c.status.running is False
    assert c.status.paused is False

    c.start()
    assert c.status.exists is True
    assert c.status.running is True
    assert c.status.paused is False

    c.remove()
    assert c.status.exists is False
    assert c.status.running is False
    assert c.status.paused is False

    assert not container_exists(c.name)

#-------------------------------------------------------------------------------
# Container context manager

def test_container():
    name = 'foobarbaz1'
    assert not container_exists(name)

    with container('mbodenhamer/alpine-data', name=name, detach=True) as c:
        assert c.name == name
        assert container_exists(name)

    assert not container_exists(name)

#-------------------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    from syn.base_utils import run_all_tests
    run_all_tests(globals(), verbose=True, print_errors=False)
