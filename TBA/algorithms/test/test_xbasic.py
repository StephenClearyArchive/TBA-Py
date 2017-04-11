#! /usr/bin/env python

# Copyright (C) 2001, Stephen Cleary
# All rights reserved.
# See the file 'COPYRIGHT' for copyright and disclaimer information

import unittest, sys, os, os.path, operator
sys.path.insert(0, os.path.join(*tuple([os.pardir] * 3)))

from TBA.algorithms.xbasic import xcat, xfilter, xmap, xunique

class CatTestCase(unittest.TestCase):
  def test_0_inputs(self):
    self.failUnless([x for x in xcat()] == [])

  def test_1_input(self):
    self.failUnless([x for x in xcat([])] == [])
    self.failUnless([x for x in xcat([3])] == [3])
    self.failUnless([x for x in xcat([3, 5, None])] == [3, 5, None])

  def test_2_inputs(self):
    self.failUnless([x for x in xcat([], [])] == [])
    self.failUnless([x for x in xcat([3], [])] == [3])
    self.failUnless([x for x in xcat([], [3])] == [3])
    self.failUnless([x for x in xcat([3, 5, None], [])] == [3, 5, None])
    self.failUnless([x for x in xcat([], [3, 5, None])] == [3, 5, None])
    self.failUnless([x for x in xcat([3, 5, None], [3])] == [3, 5, None, 3])
    self.failUnless([x for x in xcat([3], [3, 5, None])] == [3, 3, 5, None])
    self.failUnless([x for x in xcat([3, 5, None], [4, 6, 'two'])] == [3, 5, None, 4, 6, 'two'])

  def test_n_inputs(self):
    self.failUnless([x for x in xcat([1, 4, 7], [2, 5, 8], [3, 6, 9])] == [1, 4, 7, 2, 5, 8, 3, 6, 9])
    self.failUnless([x for x in xcat([2, 5, 8], [], [1, 4, 7])] == [2, 5, 8, 1, 4, 7])

class FilterTestCase(unittest.TestCase):
  def test_basic(self):
    self.failUnless([x for x in xfilter(None, [])] == [])
    self.failUnless([x for x in xfilter(None, [3])] == [3])
    self.failUnless([x for x in xfilter(None, [None, 3, [], 0, 13])] == [3, 13])

  def test_lambda(self):
    def gt_3(x): return x > 3
    self.failUnless([x for x in xfilter(gt_3, [])] == [])
    self.failUnless([x for x in xfilter(gt_3, [3])] == [])
    self.failUnless([x for x in xfilter(gt_3, [4])] == [4])
    self.failUnless([x for x in xfilter(gt_3, [2, 3, 4, 5, 6, 5, 4, 3, 2])] == [4, 5, 6, 5, 4])

class MapTestCase(unittest.TestCase):
  def test_0_inputs(self):
    self.failUnless([x for x in xmap()] == [])
    self.failUnless([x for x in xmap(None, [])] == [])
    self.failUnless([x for x in xmap(None, [], [])] == [])
    self.failUnless([x for x in xmap(None, [], [], [])] == [])

  def test_1_input(self):
    def sqr(x): return x*x
    self.failUnless([x for x in xmap(sqr, [])] == [])
    self.failUnless([x for x in xmap(sqr, [3])] == [9])
    self.failUnless([x for x in xmap(sqr, [3, 1, 2])] == [9, 1, 4])

  def test_2_inputs(self):
    add = operator.add
    self.failUnless([x for x in xmap(add, [], [])] == [])
    self.failUnless([x for x in xmap(add, [3], []).set_replace(0)] == [3])
    self.failUnless([x for x in xmap(add, [], [3]).set_replace(0)] == [3])
    self.failUnless([x for x in xmap(add, [3], [3])] == [6])
    self.failUnless([x for x in xmap(add, [3, 1, 2], [3]).set_replace(0)] == [6, 1, 2])
    self.failUnless([x for x in xmap(add, [3], [3, 1, 2]).set_replace(0)] == [6, 1, 2])
    self.failUnless([x for x in xmap(add, [6, 6, 1], [1, 2, 1])] == [7, 8, 2])

  def test_n_inputs(self):
    def add(*inputs): return reduce(operator.add, inputs)
    self.failUnless([x for x in xmap(add, [])] == [])
    self.failUnless([x for x in xmap(add, [], [])] == [])
    self.failUnless([x for x in xmap(add, [], [], [])] == [])
    self.failUnless([x for x in xmap(add, [3], [3], []).set_replace(0)] == [6])
    self.failUnless([x for x in xmap(add, [3], [], [3]).set_replace(0)] == [6])
    self.failUnless([x for x in xmap(add, [], [3], [3]).set_replace(0)] == [6])
    self.failUnless([x for x in xmap(add, [3, 4, 5], [1, 2, 3], [4, 5, 6])] == [8, 11, 14])
    self.failUnless([x for x in xmap(add, [1], [2], [3], [4])] == [10])

class UniqueTestCase(unittest.TestCase):
  def test_all(self):
    self.failUnless([x for x in xunique([])] == [])
    self.failUnless([x for x in xunique([3])] == [3])
    self.failUnless([x for x in xunique([3, 5])] == [3, 5])
    self.failUnless([x for x in xunique([3, 5, 3])] == [3, 5, 3])
    self.failUnless([x for x in xunique([3, 3, 5])] == [3, 5])
    self.failUnless([x for x in xunique([3, 5, 5])] == [3, 5])
    self.failUnless([x for x in xunique([3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 3, 3])] == [3, 5, 3])

if __name__ == '__main__':
  try:
    unittest.main()
  except SystemExit:
    pass