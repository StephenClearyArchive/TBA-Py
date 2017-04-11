# Copyright (C) 2001, Stephen Cleary
# All rights reserved.
# See the file 'COPYRIGHT' for copyright and disclaimer information

"""Various PyX algorithms.

Definitions:
  PyX input -- any iterator or iterable sequence, with the following
    restriction:
      Once it has raised StopIteration, any further calls to next() will
        also raise StopIteration. 
  PyX algorithm -- a class that is a PyX input, and computes its values
    from its own PyX input(s).

Notes:
  Any sequence type, xrange, and xreadlines are PyX inputs.

PyX Classes (each has its own __doc__):
  xcat -- Append input sequences end-to-end.
  xfilter -- Filter an input sequence.
  xmap -- Apply a function to input sequences until all of them are done.
  xmap_trim -- Apply a function to input sequences until any one is done.
  xunique -- Remove consecutive runs of equal elements in a sequence.
  xhead -- Copy part of an input sequence.
  xtail -- Copy last part of an input sequence.
  xfill -- Pad the ending of an input sequence.
"""

from xcompatibility import *
import xbase

#
# Pipe Algorithm classes
#

class xcat (xbase.xbase):
  """Append input sequences end-to-end.

  xcat can take any number of input sequences.  Its output sequence
  is those input sequences appended end-to-end.

  Methods:
    __init__(self, *inputs)
    set_inputs(self, *inputs) --
      Must be called before iteration begins.
      Returns self.

  Examples:
    >>> [x for x in xcat([1, 3, 5], [2, 4, 6])]
    [1, 3, 5, 2, 4, 6]
    >>> [x for x in xcat([1], [2, 6], [4], [3], [5, 7])]
    [1, 2, 6, 4, 3, 5, 7]
  """

  def __init__(self, *inputs):
    self.__in = map(iter, inputs)
    self.__len_in = len(inputs)
    self.__which = 0

  def next(self):
    while 1:
      if self.__which == self.__len_in:
        raise StopIteration
      try:
        return self.__in[self.__which].next()
      except StopIteration:
        self.__which += 1

  def set_inputs(self, *inputs):
    self.__in = map(iter, inputs)
    self.__len_in = len(inputs)
    return self

class xfilter (xbase.xbase):
  """Filters an input sequence.

  xfilter takes one input sequence and a filtering function.  If the
  filtering function is None, then it uses the identity function.
  (This is just like the behaviour of the builtin 'filter').

  Methods:
    __init__(self, func = None, input = None)
    set_input(self, input),
    set_func(self, func) --
      Must be called before iteration begins.
      Returns self.

  Examples:
    >>> [x for x in xfilter(None, [0, 2, 0, 4, 6, 7])]
    [2, 4, 6, 7]
    >>> [x for x in xfilter(callable, [chr, 3, [], ord])]
    [<built-in function chr>, <built-in function ord>]
  """

  def __init__(self, func = None, input = None):
    self.__in = iter(input)
    self.__func = func

  def next(self):
    while 1:
      ret = self.__in.next()
      if self.__func is None:
        if ret:
          return ret
      elif self.__func(ret):
        return ret

  def set_input(self, input):
    self.__in = iter(input)
    return self

  def set_func(self, func):
    self.__func = func
    return self

class xmap (xbase.xbase):
  """Applies a function over input sequences until all of them are done.

  xmap takes a function and any number of input sequences.  Another
  optional parameter is a replacement value, which is the value to
  substitute when one sequence is shorter than another (by default,
  None).

  The function is applied to the elements of the input sequences, in
  order.  The result sequence is the results of the function.  This
  is exactly how the builtin 'map' operates.

  Methods:
    __init__(self, func = None, *inputs) --
      Note that 'replace' is not a parameter; it *must* be set using
        set_replace.
    set_inputs(self, *inputs),
    set_func(self, func),
    set_replace(self, replace) --
      Must be called before iteration begins.
      Returns self.

  Examples:
    >>> [x for x in xmap(abs, [3, 0, -2, -1])]
    [3, 0, 2, 1]
    >>> import operator
    >>> [x for x in xmap(operator.add, [1, 2, 3], [4, 5, 6])]
    [5, 7, 9]
    >>> [x for x in xmap(operator.mul, [2, 3], [5, 7, 11])]
    Traceback ...
    TypeError: unsupported operand type(s) for *
    >>> [x for x in xmap(operator.mul, [2, 3], [5, 7, 11]).set_replace(1)]
    [10, 21, 11]
  """

  def __init__(self, func = None, *inputs):
    self.__in = map(iter, inputs)
    self.__func = func
    self.__replace = None

  def next(self):
    done = 1
    data_set = []
    for i in xrange(len(self.__in)):
      try:
        data_set.append(self.__in[i].next())
        done = 0
      except StopIteration:
        data_set.append(self.__replace)
    if done:
      raise StopIteration
    return apply(self.__func, data_set)

  def set_inputs(self, *inputs):
    self.__in = map(iter, inputs)
    return self

  def set_func(self, func):
    self.__func = func
    return self

  def set_replace(self, replace):
    self.__replace = replace
    return self

class xmap_trim (xbase.xbase):
  """Applies a function over input sequences until any of them are done.

  xmap_trim takes a function and any number of input sequences.

  The function is applied to the elements of the input sequences, in
  order.  The result sequence is the results of the function.

  Methods:
    __init__(self, func = None, *inputs)
    set_inputs(self, *inputs),
    set_func(self, func) --
      Must be called before iteration begins.
      Returns self.

  Examples:
    >>> [x for x in xmap_trim(abs, [3, 0, -2, -1])]
    [3, 0, 2, 1]
    >>> import operator
    >>> [x for x in xmap_trim(operator.add, [1, 2, 3], [4, 5, 6])]
    [5, 7, 9]
    >>> [x for x in xmap_trim(operator.mul, [2, 3], [5, 7, 11])]
    [10, 21]
  """

  def __init__(self, func = None, *inputs):
    self.__in = map(iter, inputs)
    self.__func = func
    self.__replace = None

  def next(self):
    return apply(self.__func, [x.next() for x in self.__in])

  def set_inputs(self, *inputs):
    self.__in = map(iter, inputs)
    return self

  def set_func(self, func):
    self.__func = func
    return self

class xunique (xbase.xbase):
  """Removes consecutive equivalent values from a sequence.

  xunique takes a single input sequence and an optional comparision
  function.  It produces a sequence with all consecutive equivalent
  values (as defined by the comparision function) reduced to one
  value.

  Stability: The reduced value in the output sequence is the first
  of the consecutive equivalent values in the input sequence.

  Methods:
    __init__(self, input = None, comp = cmp)
    set_input(self, input),
    set_comp(self, comp) --
      Must be called before iteration begins.
      Returns self.

  Examples:
    >>> [x for x in xunique([1, 1, 2, 3])]
    [1, 2, 3]
    >>> a = []
    >>> b = []
    >>> [x for x in xunique([a, b])]
    [[]]
    >>> result = xunique([a, b])[0]
    >>> result
    []
    >>> result is a
    1
    >>> result is b
    0
  """

  def __init__(self, input = None, comp = cmp):
    self.__in = xbase.xsingle_buffer(input)
    self.__comp = comp

  def next(self):
    ret = self.__in.consume()
    try:
      while self.__comp(ret, self.__in.get()) == 0:
        self.__in.next()
    except StopIteration:
      pass
    return ret

  def set_input(self, input):
    self.__in = xsingle_buffer(input)
    return self

  def set_comp(self, comp):
    self.__comp = comp
    return self

class xhead (xbase.xbase):
  """Copy part of an input sequence.

  xhead takes a single input sequence and a numeric parameter denoting
  how many elements of output are to be generated.  The output sequence
  is that number of elements from the input sequence.  If the numeric
  parameter is larger than the number of elements in the input sequence,
  then the output sequence is the same as the input sequence.

  The numeric parameter may be of any type; it is decremented by 1 until
  less than or equal to 0.

  Methods:
    __init__(self, input = None, bound = 0)
    set_input(self, input),
    set_bound(self, bound)
      Must be called before iteration begins.
      Returns self.

  Examples:
    >>> [x for x in xhead([1, 1, 2, 3], 2)]
    [1, 1]
    >>> [x for x in xhead([1, 1, 2, 3], 9)]
    [1, 1, 2, 3]
  """

  def __init__(self, input = None, bound = 0):
    self.__in = iter(input)
    self.__bound = bound

  def next(self):
    if self.__bound > 0:
      self.__bound -= 1
      return self.__in.next()
    raise StopIteration

  def set_input(self, input):
    self.__in = iter(input)
    return self

  def set_bound(self, bound):
    self.__bound = bound
    return self

class xfill (xbase.xbase):
  """Pad the end of an input sequence.

  xfill takes a single input sequence, a numeric parameter denoting
  how many elements of output are to be generated, and a value to
  use to fill the input sequence up to that length.  The output sequence
  is all the elements from the input sequence, followed by the number of
  fill values necessary.  If the numeric parameter is smaller than the
  number of elements in the input sequence, then the output sequence is
  the same as the input sequence.

  The numeric parameter may be of any type; it is decremented by 1 until
  less than or equal to 0.

  Methods:
    __init__(self, input = None, bound = 0, fill = None)
    set_input(self, input),
    set_bound(self, bound),
    set_fill(self, fill)
      Must be called before iteration begins.
      Returns self.

  Examples:
    >>> [x for x in xfill([1, 1, 2, 3], 2, 0)]
    [1, 1, 2, 3]
    >>> [x for x in xfill([1, 1, 2, 3], 9, 0)]
    [1, 1, 2, 3, 0, 0, 0, 0, 0]
  """

  def __init__(self, input = None, bound = 0, fill = None):
    self.__in = iter(input)
    self.__bound = bound
    self.__fill = fill

  def next(self):
    if self.__bound > 0:
      self.__bound -= 1
      try:
        return self.__in.next()
      except StopIteration:
        return self.__fill
    raise StopIteration

  def set_input(self, input):
    self.__in = iter(input)
    return self

  def set_bound(self, bound):
    self.__bound = bound
    return self

  def set_fill(self, fill):
    self.__fill = fill
    return self

class xtail (xbase.xbase):
  """Copy last part of an input sequence.

  xtail takes a single input sequence and a numeric parameter denoting
  how many elements of output are to be skipped.  The output sequence is
  the elements from the input sequence after some of the inputs were
  skipped.  If the numeric parameter is larger than the number of elements
  in the input sequence, then the output sequence is empty.

  The numeric parameter may be of any type; it is decremented by 1 until
  less than or equal to 0.

  Methods:
    __init__(self, input = None, bound = 0)
    set_input(self, input),
    set_bound(self, bound)
      Must be called before iteration begins.
      Returns self.

  Examples:
    >>> [x for x in xtail([1, 1, 2, 3], 2)]
    [2, 3]
    >>> [x for x in xtail([1, 1, 2, 3], 9)]
    []
  """

  def __init__(self, input = None, bound = 0):
    self.__in = iter(input)
    self.__bound = bound

  def next(self):
    while self.__bound > 0:
      self.__bound -= 1
      self.__in.next()
    return self.__in.next()

  def set_input(self, input):
    self.__in = iter(input)
    return self

  def set_bound(self, bound):
    self.__bound = bound
    return self
