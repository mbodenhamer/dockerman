'''Utilities for marshalling command-line arguments.
'''
import six
import threading
from contextlib import contextmanager
from collections import Iterable
from syn.base import Base, Attr

if six.PY2:
    str = unicode

#-------------------------------------------------------------------------------
# Utilities

def quote(s, quote_char):
    return quote_char + s + quote_char

#-------------------------------------------------------------------------------
# Argument list context wrapper

@contextmanager
def arglist(lst):
    with threading.Lock():
        tmp = Argument._arglist
        Argument._arglist = lst
        yield
        Argument._arglist = tmp

#-------------------------------------------------------------------------------
# Argument base class


class Argument(Base):
    _arglist = None
    _opts = dict(args = ('name',),
                 coerce_args = True,
                 optional_none = True,
                 init_validate = True)
    _attrs = dict(sep = Attr(str, u' ', 
                             'Character used to separate multiple values'),
                  quote = Attr(['always', 'multiple', 'never'], 'multiple',
                               ('Values quoting policy - either always quote, '
                                'only quote if there are multiple values, or '
                                'never quote')),
                  quote_elements = Attr(bool, False, ('Quote only the individual'
                                                      'parts of a multi-value')),
                  quote_char = Attr(["'", '"', '\"'], '"',
                                    'Character to use for quoting values'),
                  single_value = Attr(bool, False, ('Interpret value as '
                                                    'a single value')),
                  name = Attr(str, doc='The name of the argument')
                  )

    def __init__(self, *args, **kwargs):
        super(Argument, self).__init__(*args, **kwargs)

        arglist = type(self)._arglist
        if arglist is not None:
            arglist.append(self)

    def render(self, value):
        if (isinstance(value, Iterable) and not self.single_value
            and not isinstance(value, six.string_types)):
            if self.quote_elements:
                out = self.sep.join(quote(str(val), self.quote_char) 
                                    for val in value)
            else:
                out = self.sep.join(str(val) for val in value)
            multiple = True
        else:
            out = str(value)
            multiple = False

        if self.quote == 'always' or (self.quote == 'multiple' and multiple
                                      and not self.quote_elements):
            out = quote(out, self.quote_char)

        return out


#-------------------------------------------------------------------------------
# Positional argument


class Positional(Argument):
    _attrs = dict(repeatable = Attr(bool, False, ('If true, multiple values can'
                                                  ' be supplied'))
                 )

    def __init__(self, *args, **kwargs):
        super(Positional, self).__init__(*args, **kwargs)

        if not self.repeatable:
            self.quote = 'multiple'


#-------------------------------------------------------------------------------
# Option


class Option(Argument):
    _opts = dict(args = ('name', 'aliases'))
    _attrs = dict(aliases = Attr(list, doc='Other strings denoting the option',
                                 optional=True),
                  use_eq = Attr(bool, False, 'Use name=value syntax'),
                  interleave = Attr(bool, True, ('Repeat the option for '
                                                 'multiple values')),
                 )

    def __init__(self, *args, **kwargs):
        super(Option, self).__init__(*args, **kwargs)

        if self.aliases is None:
            self.aliases = []
        else:
            self.aliases = list(self.aliases)

    def render(self, value):
        multiple = False
        if (isinstance(value, Iterable) and not self.single_value
            and not isinstance(value, six.string_types)):
            multiple = True

        prefix = self.name
        if self.use_eq:
            prefix += '='
        else:
            prefix += ' '

        if multiple and self.interleave:
            strs = [super(Option, self).render(val) for val in value]
        else:
            strs = [super(Option, self).render(value)]
            
        out = ' '.join(prefix + s for s in strs)
        return out


#-------------------------------------------------------------------------------
# Binary Option


class BinaryOption(Option):
    _attrs = dict(value = Attr(bool, False, 'Value of the option')
                 )

    def render(self, value):
        out = ''
        if value:
            out = self.name

        return out


#-------------------------------------------------------------------------------
# Render arguments for invocation

def render_args(arglst, argdct):
    '''Render arguments for command-line invocation.

    arglst: A list of Argument objects (specifies order)
    argdct: A mapping of argument names to values (specifies rendered values)
    '''
    out = ''
    
    for arg in arglst:
        if arg.name in argdct:
            rendered = arg.render(argdct[arg.name])
            if rendered:
                out += ' '
                out += rendered

    return out

#-------------------------------------------------------------------------------
# __all__

__all__ = ('Argument', 'Positional', 'Option', 'BinaryOption', 
           'arglist', 'render_args')

#-------------------------------------------------------------------------------
