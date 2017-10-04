import shlex
import socket
from subprocess import Popen, PIPE
from syn.five import STR

from docker.errors import NotFound
from .base import CLIENT

#-------------------------------------------------------------------------------
# Argument processors

def join(obj=None, sep=' '):
    if isinstance(obj, list):
        return sep.join(obj)
    return obj

def split(obj=None, sep=None):
    if isinstance(obj, STR):
        return obj.split(sep)
    return obj

def dictify_strings(obj=None, empty=True, sep=None):
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

#-------------------------------------------------------------------------------
# Process utilities

def call(s):
    proc = Popen(shlex.split(s), stdout=PIPE, stderr=PIPE)
    (out, err) = proc.communicate()
    return out,err

#-------------------------------------------------------------------------------
# Network utilities

def scan_port(addr, port):
    sock = socket.socket()
    try:
        sock.settimeout(1)
        sock.connect((addr, port))
        sock.close()
        return True
    except socket.error as e:
        if e.errno == 111:  # Connection refused
            return False
        else:
            raise e

#-------------------------------------------------------------------------------
# Docker utilities

def container_exists(name, client=CLIENT):
    try:
        client.inspect_container(name)
        return True
    except NotFound:
        return False

#-------------------------------------------------------------------------------
# __all__

__all__ = ('join', 'split', 'dictify_strings', 
           'call', 
           'scan_port',
           'container_exists')

#-------------------------------------------------------------------------------
