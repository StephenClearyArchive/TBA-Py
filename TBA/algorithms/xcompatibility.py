# Copyright (C) 2001, Stephen Cleary
# All rights reserved.
# See the file 'COPYRIGHT' for copyright and disclaimer information

"""PyX compatibility definitions.

The definitions in this file must be at a reachable scope in all files
defining PyX algorithms.  Thus, for any file containing a PyX algorithm,
it should first do a 'from xcompatibility import *'.

Classes and functions are provided that allow PyX algorithms in
versions of Python before 2.2.
"""

import sys

# Support for Pythons earlier than 2.2
if sys.version_info[0] < 2 or (sys.version_info[0] == 2 and sys.version_info[1] < 2):
  SUPPORT_SEQUENCE_ITER = 1
else:
  SUPPORT_SEQUENCE_ITER = 0

#
# Provide iterators if pre-2.2
#

if SUPPORT_SEQUENCE_ITER:
  class StopIteration(Exception): pass
  class __iter:
    def __init__(self, seq):
      self.__seq = seq
      self.__i = -1
    def __iter__(self): return self
    def next(self):
      # Note: we increment i *first* to allow xreadlines to work with
      #   this class properly.
      self.__i += 1
      try:
        return self.__seq[self.__i]
      except IndexError:
        raise StopIteration
  def iter(seq):
    if hasattr(seq, '__iter__'):
      return seq.__iter__()
    return __iter(seq)
