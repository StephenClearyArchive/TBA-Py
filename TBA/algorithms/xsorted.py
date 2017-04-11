# Copyright (C) 2001, Stephen Cleary
# All rights reserved.
# See the file 'COPYRIGHT' for copyright and disclaimer information

"""PyX algorithms for sorted input streams.

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
  xmerge -- Merge two sorted sequences.
  xset_union -- Union two sorted, unique sequences (|).
  xset_intersection -- Intersect two sorted, unique sequences (&).
  xset_difference -- Difference two sorted, unique sequences (&~).
  xset_symmetric_difference -- Symm. diff. two sorted, unique sequences (^).
"""

from xcompatibility import *
import xbase

#
# Pipe Algorithm classes
#

class xmerge (xbase.xbase):
  """Merges two sorted sequences.

  Produces a sorted sequence.  Optionally can take a comparision
  object.

  Stability: If equivalent elements occur in both input sequences,
  the output sequence contains all equivalent elements from the
  first input sequence, followed by all equivalent elements from
  the second input sequence.

  Methods:
    __init__(self, input0 = None, input1 = None, comp = cmp)
    set_input0(self, input0),
    set_input1(self, input1),
    set_inputs(self, input0, input1),
    set_comp(self, comp) --
      Must be called before iteration begins.
      Returns self.

  Examples:
    >>> [x for x in xmerge([1, 4], [2, 3, 4])]
    [1, 2, 3, 4, 4]
    >>> a = []
    >>> b = []
    >>> [x for x in xmerge([a], [b])]
    [[], []]
    >>> result = xunique([a], [b])[0]
    >>> result
    []
    >>> result is a
    1
    >>> result is b
    0
  """

  def __init__(self, input0 = None, input1 = None, comp = cmp):
    self.__in0, self.__in1 = xbase.xsingle_buffer(input0), xbase.xsingle_buffer(input1)
    self.__comp = comp

  def next(self):
    try:
      x = self.__in0.get()
    except StopIteration:
      return self.__in1.consume()
    try:
      y = self.__in1.get()
    except StopIteration:
      self.__in0.next()
      return x
    if self.__comp(x, y) > 0:
      self.__in1.next()
      return y
    else:
      self.__in0.next()
      return x

  def set_input0(self, input0):
    self.__in0 = xbase.xsingle_buffer(input0)
    return self

  def set_input1(self, input1):
    self.__in1 = xbase.xsingle_buffer(input1)
    return self

  def set_inputs(self, input0, input1):
    self.__in0, self.__in1 = xbase.xsingle_buffer(input0), xbase.xsingle_buffer(input1)
    return self

  def set_comp(self, comp):
    self.__comp = comp
    return self

class xset_union (xbase.xbase):
  """Unions two sorted, unique sequences ("or").

  Produces a sorted, unique sequence.  Optionally can take a
  comparision object.

  Stability: If equivalent elements occur in both input sequences,
  the output sequence contains the element from the first input
  sequence.

  Methods:
    __init__(self, input0 = None, input1 = None, comp = cmp)
    set_input0(self, input0),
    set_input1(self, input1),
    set_inputs(self, input0, input1),
    set_comp(self, comp) --
      Must be called before iteration begins.
      Returns self.

  Examples:
    >>> [x for x in xset_union([1, 4], [2, 3, 4])]
    [1, 2, 3, 4]
    >>> a = []
    >>> b = []
    >>> [x for x in xset_union([a], [b])]
    [[]]
    >>> result = xset_union([a], [b])[0]
    >>> result
    []
    >>> result is a
    1
    >>> result is b
    0
  """

  def __init__(self, input0 = None, input1 = None, comp = cmp):
    self.__in0, self.__in1 = xbase.xsingle_buffer(input0), xbase.xsingle_buffer(input1)
    self.__comp = comp

  def next(self):
    try:
      x = self.__in0.get()
    except StopIteration:
      return self.__in1.consume()
    try:
      y = self.__in1.get()
    except StopIteration:
      self.__in0.next()
      return x
    c = self.__comp(x, y)
    if c > 0:
      self.__in1.next()
      return y
    elif c < 0:
      self.__in0.next()
      return x
    else:
      self.__in0.next()
      self.__in1.next()
      return x

  def set_input0(self, input0):
    self.__in0 = xbase.xsingle_buffer(input0)
    return self

  def set_input1(self, input1):
    self.__in1 = xbase.xsingle_buffer(input1)
    return self

  def set_inputs(self, input0, input1):
    self.__in0, self.__in1 = xbase.xsingle_buffer(input0), xbase.xsingle_buffer(input1)
    return self

  def set_comp(self, comp):
    self.__comp = comp
    return self

class xset_intersection (xbase.xbase):
  """Intersects two sorted, unique sequences ("and").

  Produces a sorted, unique sequence.  Optionally can take a
  comparision object.

  Stability: All elements in the output sequence are copied
  from the first input sequence.

  Methods:
    __init__(self, input0 = None, input1 = None, comp = cmp)
    set_input0(self, input0),
    set_input1(self, input1),
    set_inputs(self, input0, input1),
    set_comp(self, comp) --
      Must be called before iteration begins.
      Returns self.

  Examples:
    >>> [x for x in xset_intersection([1, 4], [2, 3, 4])]
    [4]
    >>> a = []
    >>> b = []
    >>> [x for x in xset_intersection([a], [b])]
    [[]]
    >>> result = xset_intersection([a], [b])[0]
    >>> result
    []
    >>> result is a
    1
    >>> result is b
    0
  """

  def __init__(self, input0 = None, input1 = None, comp = cmp):
    self.__in0, self.__in1 = xbase.xsingle_buffer(input0), xbase.xsingle_buffer(input1)
    self.__comp = comp

  def next(self):
    x, y = self.__in0.get(), self.__in1.get()
    while 1:
      c = self.__comp(x, y)
      if c > 0:
        self.__in1.next()
        y = self.__in1.get()
      elif c < 0:
        self.__in0.next()
        x = self.__in0.get()
      else:
        self.__in0.next()
        self.__in1.next()
        return x

  def set_input0(self, input0):
    self.__in0 = xbase.xsingle_buffer(input0)
    return self

  def set_input1(self, input1):
    self.__in1 = xbase.xsingle_buffer(input1)
    return self

  def set_inputs(self, input0, input1):
    self.__in0, self.__in1 = xbase.xsingle_buffer(input0), xbase.xsingle_buffer(input1)
    return self

  def set_comp(self, comp):
    self.__comp = comp
    return self

class xset_difference (xbase.xbase):
  """Calculates the difference of two sorted, unique sequences ("and not").

  Produces a sorted, unique sequence.  Optionally can take a
  comparision object.

  Methods:
    __init__(self, input0 = None, input1 = None, comp = cmp)
    set_input0(self, input0),
    set_input1(self, input1),
    set_inputs(self, input0, input1),
    set_comp(self, comp) --
      Must be called before iteration begins.
      Returns self.

  Examples:
    >>> [x for x in xset_difference([1, 4], [2, 3, 4])]
    [1]
    >>> [x for x in xset_difference([2, 3, 4], [1, 4])]
    [2, 3]
  """

  def __init__(self, input0 = None, input1 = None, comp = cmp):
    self.__in0, self.__in1 = iter(input0), xbase.xsingle_buffer(input1)
    self.__comp = comp

  def next(self):
    x = self.__in0.next()
    while 1:
      try:
        y = self.__in1.get()
      except StopIteration:
        return x
      c = self.__comp(x, y)
      if c > 0:
        self.__in1.next()
      elif c < 0:
        return x
      else:
        x = self.__in0.next()
        self.__in1.next()

  def set_input0(self, input0):
    self.__in0 = iter(input0)
    return self

  def set_input1(self, input1):
    self.__in1 = xbase.xsingle_buffer(input1)
    return self

  def set_inputs(self, input0, input1):
    self.__in0, self.__in1 = iter(input0), xbase.xsingle_buffer(input1)
    return self

  def set_comp(self, comp):
    self.__comp = comp
    return self

class xset_symmetric_difference (xbase.xbase):
  """Calculates the symm. diff. of two sorted, unique sequences ("xor").

  Produces a sorted, unique sequence.  Optionally can take a
  comparision object.

  Methods:
    __init__(self, input0 = None, input1 = None, comp = cmp)
    set_input0(self, input0),
    set_input1(self, input1),
    set_inputs(self, input0, input1),
    set_comp(self, comp) --
      Must be called before iteration begins.
      Returns self.

  Example:
    >>> [x for x in xset_symmetric_difference([1, 4], [2, 3, 4])]
    [1, 2, 3]
  """

  def __init__(self, input0 = None, input1 = None, comp = cmp):
    self.__in0, self.__in1 = xbase.xsingle_buffer(input0), xbase.xsingle_buffer(input1)
    self.__comp = comp

  def next(self):
    while 1:
      try:
        x = self.__in0.get()
      except StopIteration:
        return self.__in1.consume()
      try:
        y = self.__in1.get()
      except StopIteration:
        self.__in0.next()
        return x
      c = self.__comp(x, y)
      if c > 0:
        self.__in1.next()
        return y
      elif c < 0:
        self.__in0.next()
        return x
      else:
        self.__in0.next()
        self.__in1.next()

  def set_input0(self, input0):
    self.__in0 = xbase.xsingle_buffer(input0)
    return self

  def set_input1(self, input1):
    self.__in1 = xbase.xsingle_buffer(input1)
    return self

  def set_inputs(self, input0, input1):
    self.__in0, self.__in1 = xbase.xsingle_buffer(input0), xbase.xsingle_buffer(input1)
    return self

  def set_comp(self, comp):
    self.__comp = comp
    return self
