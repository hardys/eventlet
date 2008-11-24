import unittest
from eventlet.api import sleep, spawn, kill

DELAY = 0.1

class Test(unittest.TestCase):

    def test_killing_dormant(self):
        state = []
        def test():
            try:
                state.append('start')
                sleep(DELAY)
            except:
                state.append('except')
                # catching GreenletExit
                pass
            # when switching to hub, hub makes itself the parent of this greenlet,
            # thus after the function's done, the control will go to the parent
            # QQQ why the first sleep is not enough?
            sleep(0)
            state.append('finished')
        g = spawn(test)
        sleep(DELAY/2)
        assert state == ['start'], state
        kill(g)
        # will not get there, unless switching is explicitly scheduled by kill
        assert state == ['start', 'except'], state
        sleep(DELAY)
        assert state == ['start', 'except', 'finished'], state

if __name__=='__main__':
    unittest.main()
