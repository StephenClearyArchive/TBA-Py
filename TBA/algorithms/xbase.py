# Copyright (C) 2001, Stephen Cleary
# All rights reserved.
# See the file 'COPYRIGHT' for copyright and disclaimer information

"""PyX helper definitions.

Helper Classes (each has its own __doc__):
  xsingle_buffer -- Helper class for writing some PyX algorithms.
  xbase -- Helper base class for writing PyX algorithms.

Global Functions (each has its own __doc__):
  xresult -- Create in-memory sequence from PyX input.
"""

import types

from xcompatibility import *

#
# Utility classes
#

class xsingle_buffer:
  """Helper class for writing some PyX algorithms.

  Many PyX algorithms need to buffer their input(s), but only need a
  single-element buffer.  This class acts as a wrapper around a PyX
  input, providing that single-element buffer.  The buffer is read
  through the member function "get()", and the iterator is incremented
  through the member function "next()".  Whether or not "get()" will
  throw can be determined by converting that object to a truth value.
  If it evaluates to 1, then "get()" will not throw.

  "next()" returns self.

  Once StopIteration is raised, you can continue to call "get()" and
  testing it for truth value, but do not call "next()".

  Methods (each has its own __doc__):
    __init__ -- Create an xsingle_buffer.
    get -- Return buffer of an xsingle_buffer.
    next -- Clear buffer of an xsingle_buffer.
    __nonzero__ -- Test an xsingle_buffer.
    consume -- Return and clear buffer of an xsingle_buffer.

  Examples:
    >>> def true(x):
    ...   if x: return 1
    ...   else: return 0
    ... 
    >>> i = xsingle_buffer([1, 2, 3])
    >>> true(i)
    1
    >>> i.get()
    1
    >>> true(i)
    1
    >>> i.next()
    <xsingle_buffer instance at ...>
    >>> true(i)
    1
    >>> i.get()
    2
    >>> i.get()
    2
    >>> true(i)
    1
    >>> i.next()
    <xsingle_buffer instance at ...>
    >>> true(i)
    1
    >>> i.get()
    3
    >>> true(i)
    1
    >>> i.next()
    <xsingle_buffer instance at ...>
    >>> true(i)
    0
    >>> i.get()
    Traceback ...
    StopIteration
    >>> true(i)
    0
    >>> i.get()
    Traceback ...
    StopIteration
  """

  def __init__(self, input):
    """Create an xsingle_buffer.

    Arguments:
      input -- The PyX input to wrap around.

    Notes:
      After this function is called, the buffer is empty.
    """

    self.__in = iter(input)
    self.__valid = 0

  def get(self):
    """Return buffer of an xsingle_buffer.

    Arguments: none.

    Returns: buffer value.

    Notes:
      If the buffer is empty, loads a value into the buffer;
        then returns the buffer.
      Raises StopIteration if the input is exhausted.
    """

    if not self.__valid:
      self.__val = self.__in.next()
      self.__valid = 1
    return self.__val

  def next(self):
    """Clear buffer of an xsingle_buffer.

    Arguments: none.

    Returns: self.

    Notes:
      Empties the buffer.  This does *not* load a value into
        the buffer.
      Does not raise exceptions.
    """

    self.__valid = 0
    return self

  def __nonzero__(self):
    """Test an xsingle_buffer.

    Arguments: none.

    Returns: 1 if get() can be called without throwing, 0 otherwise.

    Notes:
      Does not raise StopIteration.
    """

    try:
      self.get()
    except StopIteration:
      return 0
    return 1

  def consume(self):
    """Return and clear buffer of an xsingle_buffer.

    Equivalent to calling get(), followed by next().

    Arguments: none.

    Returns: Same as get().

    Notes:
      If get() raises an exception, next() is *not* called.  In that
      case, consume() is equivalent to get().
    """

    ret = self.get()
    self.next()
    return ret

class xbase:
  """Base class for PyX algorithms.

  PyX algorithms do not *have* to derive from this class,
  but it may be helpful.  This class just defines __iter__
  to return self, and (if running Python earlier than 2.2)
  defines __getitem__ to just call next(), translating
  StopIteration into IndexError.
  """

  def __iter__(self): return self
  if SUPPORT_SEQUENCE_ITER:
    def __getitem__(self, i):
      try:
        return self.next()
      except StopIteration:
        raise IndexError

#
# Global functions
#

def xresult(input, start = None):
  """Create in-memory sequence from PyX input.

  Arguments:
    input --
      The PyX input to use.
    start (optional) --
      The sequence on which the PyX input is concatenated.
      Must be of string, tuple, or list type.  If 'None',
      a starting value of '[]' is used.  Defaults to 'None'.
      The value of this argument (if mutable) may be changed.

  Returns:
    A sequence starting with 'start' that also contains each
    element in 'input'.

  Notes:
    The expression 'xresult(inp)' is equivalent to:
    '[x for x in inp]'
    
  Example:
    >>> xresult( xcat([1, 3, 5], [2, 4, 6]) )
    [1, 3, 5, 2, 4, 6]
  """

  if start is None:
    return [x for x in input]
  elif type(start) is types.StringType:
    while 1:
      try:
        start += input.next()
      except StopIteration:
        return start
  elif type(start) is types.TupleType:
    while 1:
      try:
        start += ( input.next(), )
      except StopIteration:
        return start
  else:
    return start + [x for x in input]
