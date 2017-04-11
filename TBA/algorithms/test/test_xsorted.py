#! /usr/bin/env python

# Copyright (C) 2001, Stephen Cleary
# All rights reserved.
# See the file 'COPYRIGHT' for copyright and disclaimer information

import unittest, sys, os, os.path
sys.path.insert(0, os.path.join(*tuple([os.pardir] * 3)))

from TBA.algorithms.xsorted import xmerge, xset_union, xset_intersection, \
    xset_difference, xset_symmetric_difference

class MergeTestCase(unittest.TestCase):
  def test_all(self):
    self.failUnless([x for x in xmerge([], [])] == [])
    self.failUnless([x for x in xmerge([3], [])] == [3])
    self.failUnless([x for x in xmerge([], [3])] == [3])
    self.failUnless([x for x in xmerge([3], [3])] == [3, 3])
    self.failUnless([x for x in xmerge([2, 4], [1, 3, 5, 7])] == [1, 2, 3, 4, 5, 7])
    self.failUnless([x for x in xmerge([2, 4], [3, 5, 7])] == [2, 3, 4, 5, 7])
    self.failUnless([x for x in xmerge([1, 3, 5, 7], [2, 4])] == [1, 2, 3, 4, 5, 7])
    self.failUnless([x for x in xmerge([3, 5, 7], [2, 4])] == [2, 3, 4, 5, 7])
    a, b = [], []
    result = [x for x in xmerge([a], [b])]
    self.failUnless(result == [[], []])
    self.failUnless(result[0] is a)
    self.failUnless(result[1] is b)

class SetUnionTestCase(unittest.TestCase):
  def test_all(self):
    self.failUnless([x for x in xset_union([], [])] == [])
    self.failUnless([x for x in xset_union([1], [])] == [1])
    self.failUnless([x for x in xset_union([], [1])] == [1])
    self.failUnless([x for x in xset_union([1], [1])] == [1])
    self.failUnless([x for x in xset_union([2, 4], [1, 3, 5, 7])] == [1, 2, 3, 4, 5, 7])
    self.failUnless([x for x in xset_union([2, 4], [3, 5, 7])] == [2, 3, 4, 5, 7])
    self.failUnless([x for x in xset_union([1, 3, 5, 7], [2, 4])] == [1, 2, 3, 4, 5, 7])
    self.failUnless([x for x in xset_union([3, 5, 7], [2, 4])] == [2, 3, 4, 5, 7])
    a, b = [], []
    result = [x for x in xset_union([a], [b])]
    self.failUnless(result == [[]])
    self.failUnless(result[0] is a)

class SetIntersectionTestCase(unittest.TestCase):
  def test_all(self):
    self.failUnless([x for x in xset_intersection([], [])] == [])
    self.failUnless([x for x in xset_intersection([1], [])] == [])
    self.failUnless([x for x in xset_intersection([], [1])] == [])
    self.failUnless([x for x in xset_intersection([1], [1])] == [1])
    self.failUnless([x for x in xset_intersection([2, 4], [1, 3, 5])] == [])
    self.failUnless([x for x in xset_intersection([1, 3, 5], [2, 4])] == [])
    self.failUnless([x for x in xset_intersection([1, 3, 5], [2, 3, 4, 5])] == [3, 5])
    self.failUnless([x for x in xset_intersection([3, 5], [3, 4, 5])] == [3, 5])
    a, b = [], []
    result = [x for x in xset_intersection([a], [b])]
    self.failUnless(result == [[]])
    self.failUnless(result[0] is a)

class SetDifferenceTestCase(unittest.TestCase):
  def test_all(self):
    self.failUnless([x for x in xset_difference([], [])] == [])
    self.failUnless([x for x in xset_difference([1], [])] == [1])
    self.failUnless([x for x in xset_difference([], [1])] == [])
    self.failUnless([x for x in xset_difference([1], [1])] == [])
    self.failUnless([x for x in xset_difference([1, 2, 3, 4], [0])] == [1, 2, 3, 4])
    self.failUnless([x for x in xset_difference([1, 2, 3, 4], [1])] == [2, 3, 4])
    self.failUnless([x for x in xset_difference([1, 2, 3, 4], [2])] == [1, 3, 4])
    self.failUnless([x for x in xset_difference([1, 2, 3, 4], [3])] == [1, 2, 4])
    self.failUnless([x for x in xset_difference([1, 2, 3, 4], [4])] == [1, 2, 3])
    self.failUnless([x for x in xset_difference([1, 2, 3, 4], [5])] == [1, 2, 3, 4])
    self.failUnless([x for x in xset_difference([1, 2, 3, 4], [2, 3])] == [1, 4])
    self.failUnless([x for x in xset_difference([1, 2, 3, 4], [2, 4, 5])] == [1, 3])

class SetSymmetricDifferenceTestCase(unittest.TestCase):
  def test_all(self):
    self.failUnless([x for x in xset_symmetric_difference([], [])] == [])
    self.failUnless([x for x in xset_symmetric_difference([1], [])] == [1])
    self.failUnless([x for x in xset_symmetric_difference([], [1])] == [1])
    self.failUnless([x for x in xset_symmetric_difference([1], [1])] == [])
    self.failUnless([x for x in xset_symmetric_difference([1, 2, 3, 4], [0])] == [0, 1, 2, 3, 4])
    self.failUnless([x for x in xset_symmetric_difference([0], [1, 2, 3, 4])] == [0, 1, 2, 3, 4])
    self.failUnless([x for x in xset_symmetric_difference([1, 2, 3, 4], [1])] == [2, 3, 4])
    self.failUnless([x for x in xset_symmetric_difference([1], [1, 2, 3, 4])] == [2, 3, 4])
    self.failUnless([x for x in xset_symmetric_difference([1, 2, 3, 4], [2])] == [1, 3, 4])
    self.failUnless([x for x in xset_symmetric_difference([2], [1, 2, 3, 4])] == [1, 3, 4])
    self.failUnless([x for x in xset_symmetric_difference([1, 2, 3, 4], [3])] == [1, 2, 4])
    self.failUnless([x for x in xset_symmetric_difference([3], [1, 2, 3, 4])] == [1, 2, 4])
    self.failUnless([x for x in xset_symmetric_difference([1, 2, 3, 4], [4])] == [1, 2, 3])
    self.failUnless([x for x in xset_symmetric_difference([4], [1, 2, 3, 4])] == [1, 2, 3])
    self.failUnless([x for x in xset_symmetric_difference([1, 2, 3, 4], [5])] == [1, 2, 3, 4, 5])
    self.failUnless([x for x in xset_symmetric_difference([5], [1, 2, 3, 4])] == [1, 2, 3, 4, 5])
    self.failUnless([x for x in xset_symmetric_difference([1, 2, 3, 4], [2, 3])] == [1, 4])
    self.failUnless([x for x in xset_symmetric_difference([2, 3], [1, 2, 3, 4])] == [1, 4])
    self.failUnless([x for x in xset_symmetric_difference([1, 2, 3, 4], [2, 4, 5])] == [1, 3, 5])
    self.failUnless([x for x in xset_symmetric_difference([2, 4, 5], [1, 2, 3, 4])] == [1, 3, 5])

if __name__ == '__main__':
  try:
    unittest.main()
  except SystemExit:
    pass