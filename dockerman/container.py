'''Representation of a Docker container.
'''

import six
from functools import partial
from syn.base import Base, Attr
from syn.utils.cmdargs import (Positional, Option, BinaryOption, arglist, 
                               render_args)

if six.PY2:
    str = unicode

OAttr = partial(Attr, optional=True)

#-------------------------------------------------------------------------------
# Container attributes

container_attrs = \
dict(image = Attr(str, doc='The image to run'),
     command = OAttr((str, list), doc='The command to be run in the container'),
     detach = Attr(bool, False, 'Detached mode'),
     tty = Attr(bool, False, 'Allocate a pseudo-TTY'),
     stdin_open = Attr(bool, False, 'Keep STDIN open even if not attached'),
     name = OAttr(str, doc='A name for the container'),
     volumes_from = OAttr(list, doc=("List of container names "
                                     "or Ids to get volumes from")),
    )

#-------------------------------------------------------------------------------
# Run args

RUN_ARGS = []
with arglist(RUN_ARGS):
    RUN_ARGD = dict(detach = BinaryOption('-d'),
                    tty = BinaryOption('-t'),
                    stdin_open = BinaryOption('-i'),
                    volumes_from = Option('--volumes-from'),
                    name = Option('--name', interleave=False),
                    image = Positional('image'),
                    command = Positional('command', quote='never')
                   )

#-------------------------------------------------------------------------------
# Container


class Container(Base):
    _attrs = container_attrs
    _opts = dict(args = ('image', 'command'),
                 coerce_args = True,
                 init_validate = True,
                 optional_none = True)
    
    def marshal_args(self):
        values = {RUN_ARGD[attr].name: val for attr, val 
                  in self.to_dict().items() if val is not None}
        return render_args(RUN_ARGS, values)


#-------------------------------------------------------------------------------
# __all__

__all__ = ('Container',)

#-------------------------------------------------------------------------------
