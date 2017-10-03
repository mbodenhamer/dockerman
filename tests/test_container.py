from time import sleep
from dockerman import Container

#-------------------------------------------------------------------------------
# Container start/stop/etc.

def test_container_start_stop():
    c = Container('mbodenhamer/alpine-data', detach=True)
    assert c.status.exists is False
    
    c.run()
    sleep(0.2)
    assert c.status.exists is True
    assert c.status.running is True
    assert c.status.paused is False

    c.pause()
    sleep(0.05)
    assert c.status.exists is True
    assert c.status.running is True
    assert c.status.paused is True

    c.unpause()
    sleep(0.05)
    assert c.status.exists is True
    assert c.status.running is True
    assert c.status.paused is False

    c.stop()
    sleep(0.2)
    assert c.status.exists is True
    assert c.status.running is False
    assert c.status.paused is False

    c.start()
    sleep(0.2)
    assert c.status.exists is True
    assert c.status.running is True
    assert c.status.paused is False

    c.remove()
    sleep(0.2)
    assert c.status.exists is False
    assert c.status.running is False
    assert c.status.paused is False

#-------------------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    from syn.base_utils import run_all_tests
    run_all_tests(globals(), verbose=True, print_errors=False)
