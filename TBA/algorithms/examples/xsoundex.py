# Copyright (C) 2001, Stephen Cleary
# All rights reserved.
# See the file 'COPYRIGHT' for copyright and disclaimer information

"""Soundex algorithm as an iterator adapter.

Global Classes (each has its own __doc__):
  xsoundex -- Calculate standard soundex code.
  xunorthodox_soundex -- Calculate (IMHO) more useful soundex code.
"""  

import string
from TBA.algorithms.xcompatibility import *
from TBA.algorithms.xbase import xbase
from TBA.algorithms.xbasic import xcat, xfill, xhead, xtail

# Dictionary entries:
#  <not present> -- the character acts as a separator
#  'S' -- the character is skipped (ignored)
#  any other char -- the resulting character for the soundex code
#  The difference between 'S' and <not present> is that adjacent consonant sounds
#    are ignored unless there's a separator character (<not present>) in-between:
#      BB  -> 1
#      BHB -> 1 (skip character 'H' doesn't separate)
#      BAB -> 11 (separator character 'A' does separate)
_soundex_dict = {
    'H':'S', 'W':'S', 
    'h':'S', 'w':'S', 

    'B':'1', 'F':'1', 'P':'1', 'V':'1',
    'b':'1', 'f':'1', 'p':'1', 'v':'1',
    'C':'2', 'G':'2', 'J':'2', 'K':'2', 'Q':'2', 'S':'2', 'X':'2', 'Z':'2',
    'c':'2', 'g':'2', 'j':'2', 'k':'2', 'q':'2', 's':'2', 'x':'2', 'z':'2',
    'D':'3', 'T':'3',
    'd':'3', 't':'3',
    'L':'4',
    'l':'4',
    'M':'5', 'N':'5',
    'm':'5', 'n':'5',
    'R':'6',
    'r':'6'
}

class xunorthodox_soundex (xbase):
  """Calculates (IMHO) more useful soundex code.

  Takes a stream of characters for which to generate the code.  Any
  characters not in the set [A-Za-z] are considered to be separator
  characters.

  Generates a soundex-like code, as a stream of characters.  The
  returned code is exactly like soundex, except that it does not
  treat initial characters specially, and will not contain a dash.
  That is, this algorithms calculates the numerical portion of the
  soundex code.

  Methods:
    __init__(self, input = None)
    set_input(self, input) --
      Must be called before iteration begins.
      Returns self.
  """

  def __init__(self, input = None):
    self.__in = iter(input)
    self.__last_char = 'X'

  def next(self):
    while (1):
      try:
        new_char = _soundex_dict[self.__in.next()]
      except KeyError:
        self.__last_char = 'X'
      else:
        if new_char != 'S' and new_char != self.__last_char:
          self.__last_char = new_char
          return new_char

  def set_input(self, input):
    self.__in = iter(input)
    return self

class xsoundex (xbase):
  """Calculates standard soundex code.

  Takes a stream of characters for which to generate the code.  Any
  characters not in the set [A-Za-z] are considered to be separator
  characters.

  Generates the standard soundex code, as a stream of characters.
  The returned code is always the first character of the input stream,
  followed by a dash, followed by exactly three digits.

  Methods:
    __init__(self, input)
    set_input(self, input) --
      Must be called before iteration begins.
      Returns self.
  """

  def __init__(self, input):
    self.__in = iter(input)
    self.__me = None

  def next(self):
    if self.__me is None:
      # We look at the first character; this determines how we
      #  calculate the rest of the code.
      tmp_char = self.__in.next()

      # See if the first character is a skip or separator char
      try:
        last_char = _soundex_dict[tmp_char]
      except KeyError:
        last_char = 'S'

      # Prepend the first character back onto the input stream
      source = xcat(tmp_char, self.__in)

      # "Call" the unorthodox soundex (calculates numerical part),
      source = xunorthodox_soundex(source)

      # If the first character is a skip or separator, then use
      #  the unorthodox soundex directly.  If it's a normal char,
      #  then strip the first character off the unorthodox soundex
      #  result.
      if last_char != 'S':
        source = xtail(source, 1)
      
      # Prepend the initial char (uppercased) and the dash
      source = xcat(string.upper(tmp_char) + '-', source)

      # Make length exactly 5, filling with '0' as necessary
      source = xhead(xfill(source, 5, '0'), 5)

      # Save algorithm for future calls
      self.__me = source

    return self.__me.next()

  def set_input(self, input):
    self.__in = iter(input)
    return self
