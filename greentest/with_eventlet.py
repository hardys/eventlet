#!/usr/bin/python
"""Execute python script with hub installed.

Usage: %prog [--hub HUB] [--reactor REACTOR] program.py
"""
import sys
import optparse

def import_green(modulename):
    m = __import__('eventlet.green.' + modulename)
    m = m.green.getattr(modulename)
    return m

def import_reactor(reactor):
    m = __import__('twisted.internet.' + reactor)
    return getattr(m.internet, reactor)

def setup_hub(hub, reactor):
    if reactor is not None:
        import_reactor(reactor).install()
    if hub is not None:
        from eventlet.api import use_hub
        use_hub(hub)

def parse_args():
    hub = None
    reactor = None
    del sys.argv[0] # kill with_eventlet.py
    if sys.argv[0]=='--hub':
        del sys.argv[0]
        hub = sys.argv[0]
        del sys.argv[0]
    if sys.argv[0]=='--reactor':
        del sys.argv[0]
        reactor = sys.argv[0]
        del sys.argv[0]
    return hub, reactor

if __name__=='__main__':
    hub, reactor = parse_args()
    setup_hub(hub, reactor)
    from eventlet.api import get_hub
    hub = get_hub() # set up the hub now
    print '===HUB=%r' % hub
    if 'twisted.internet.reactor' in sys.modules:
        print '===REACTOR=%r' % sys.modules['twisted.internet.reactor']
    sys.stdout.flush()
    execfile(sys.argv[0])
