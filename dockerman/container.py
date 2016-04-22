'''Representation of a Docker container.
'''

from functools import partial
from syn.five import STR
from syn.base import Base, Attr
from syn.utils.cmdargs import (Positional, Option, BinaryOption, arglist, 
                               render_args)
from syn.type import List, Dict
from .utils import join, split, dictify_strings

OAttr = partial(Attr, optional=True)
comma_split = partial(split, sep=',')
dictify_eqstrings = partial(dictify_strings, empty=False, sep='=')
Single = partial(Option, interleave=False)

#-------------------------------------------------------------------------------
# Group names

RA = 'run_args'
CC = 'create_container'
HC = 'host_config'

#-------------------------------------------------------------------------------
# Container attributes

container_attrs = \
dict(image = Attr(STR, doc='The image to run', groups=(RA, CC)),
     command = OAttr(STR, call=join, groups=(RA, CC),
                     doc='The command to be run in the container'),
     hostname = OAttr(STR, doc="Optional hostname for the container",
                      groups=(RA, CC)),
     user = OAttr((STR, int), doc="Username or UID", groups=(RA, CC)),
     detach = Attr(bool, False, 'Detached mode', groups=(RA, CC)),
     stdin_open = Attr(bool, False, 'Keep STDIN open even if not attached',
                       groups=(RA, CC)),
     tty = Attr(bool, False, 'Allocate a pseudo-TTY', groups=(RA, CC)),
     mem_limit = OAttr((float, STR), doc="Memory limit", groups=(RA, CC)),
     ports = OAttr(List(int), doc="A list of port numbers", groups=(CC,)),
     environment = OAttr(Dict(STR), call=dictify_eqstrings, groups=(RA, CC),
                         doc='Environment variables to set in the container'),
     dns = OAttr(List(STR), call=comma_split, doc='DNS name servers',
                 groups=(RA, CC)),
     volumes = OAttr(List(STR), call=comma_split, doc='Volume names', 
                     groups=(RA, CC)),
     volumes_from = OAttr(List(STR), doc="List of container names or Ids to "
                          "get volumes from", call=comma_split, 
                          groups=(RA, CC)),
     network_disabled = Attr(bool, False, "Disable networking", groups=(RA, CC)),
     name = OAttr(STR, doc='A name for the container', groups=(RA, CC)),
     entrypoint = OAttr(STR, call=join, doc='Container entrypoint',
                        groups=(RA, CC)),
     cpu_shares = OAttr(int, doc='CPU shares (relative weight)', 
                        groups=(RA, CC)),
     working_dir = OAttr(STR, doc='Path to working directory', groups=(RA, CC)),
     domainname = OAttr(STR, call=split, doc='Custom DNS search domains', 
                        groups=(CC,)),
     memswap_limit = OAttr(int, groups=(RA, CC)),
     mac_address = OAttr(STR, doc='MAC address to assign to the container', 
                         groups=(RA, CC)),
     labels = OAttr(Dict(STR), call=dictify_strings, groups=(RA, CC),
                    doc='A dictionary of name-value labels'),
     volume_driver = OAttr(STR, doc='The name of a volume driver/plugin', 
                           groups=(RA, CC)),
     stop_signal = OAttr(STR, doc='The signal used to stop the container', 
                         groups=(RA, CC)),
    )

#-------------------------------------------------------------------------------
# Run args

RUN_ARGS = []
with arglist(RUN_ARGS):
    RUN_ARGD = dict(detach = BinaryOption('-d'),
                    tty = BinaryOption('-t'),
                    stdin_open = BinaryOption('-i'),
                    hostname = Single('-h'),
                    user = Single('-u'),
                    mem_limit = Single('-m'),
                    environment = Option('-e'),
                    dns = Option('--dns'),
                    volumes = Option('-v'),
                    volumes_from = Option('--volumes-from'),
                    # network_disable = Literal('--net none')
                    name = Single('--name'),
                    entrypoint = Single('--entrypoint'),
                    cpu_shares = Single('--cpu-shares'),
                    working_dir = Single('-w'),
                    memswap_limit = Single('--memory-swap'),
                    mac_address = Single('--mac-address'),
                    labels = Option('-l'),
                    volume_driver = Single('--volume-driver'),
                    stop_signal = Single('--stop-signal'),
                    image = Positional('image'),
                    command = Positional('command', quote='never')
                   )

#-------------------------------------------------------------------------------
# Container


class Container(Base):
    _attrs = container_attrs
    _groups = (RA, CC, HC)
    _opts = dict(args = ('image', 'command'),
                 coerce_args = True,
                 init_validate = True,
                 optional_none = True)
    
    def marshal_args(self, group):
        if group == RA:
            values = {RUN_ARGD[attr].name: val for attr, val 
                      in self.to_dict(group, include=True).items() 
                      if val is not None}
            return render_args(RUN_ARGS, values)

        if group == HC:
            dct = {attr:val for attr, val in
                   self.to_dict(group, include=True).items() if val is not None}
            return dct

        if group == CC:
            hc = self.marshal_args(HC)
            dct = {attr: val for attr, val in 
                   self.to_dict(group, include=True).items() if val is not None}
            dct['host_config'] = hc
            return dct

        raise ValueError('Invalid group: {}'.format(group))

#-------------------------------------------------------------------------------
# __all__

__all__ = ('Container',)

#-------------------------------------------------------------------------------
