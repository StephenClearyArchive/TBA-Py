#! /usr/bin/env python

# Copyright (C) 2001, Stephen Cleary
# All rights reserved.
# See the file 'COPYRIGHT' for copyright and disclaimer information

import unittest, sys, os, os.path
sys.path.insert(0, os.path.join(*tuple([os.pardir] * 4)))
sys.path.insert(0, os.pardir)

from TBA.algorithms.xbase import xresult
from xsoundex import xsoundex

class SoundexTestCase(unittest.TestCase):
  def test_known_results(self):
    # This is a bunch of results for soundex(..) posted on the
    #  Internet.  Used here as a test suite.
    self.failUnless(xresult(xsoundex('Allricht'), '') == 'A-462')
    self.failUnless(xresult(xsoundex('Ashcraft'), '') == 'A-261')
    self.failUnless(xresult(xsoundex('Beadles'), '') == 'B-342')
    self.failUnless(xresult(xsoundex('Callahan'), '') == 'C-450')
    self.failUnless(xresult(xsoundex('Cook'), '') == 'C-200')
    self.failUnless(xresult(xsoundex('Dances'), '') == 'D-522')
    self.failUnless(xresult(xsoundex('Deusen'), '') == 'D-250')
    self.failUnless(xresult(xsoundex('Devanter'), '') == 'D-153')
    self.failUnless(xresult(xsoundex('De Vanter'), '') == 'D-153')
    self.failUnless(xresult(xsoundex('Eberhard'), '') == 'E-166')
    self.failUnless(xresult(xsoundex('Engebrethson'), '') == 'E-521')
    self.failUnless(xresult(xsoundex('Gutierrez'), '') == 'G-362')
    self.failUnless(xresult(xsoundex('Heimbach'), '') == 'H-512')
    self.failUnless(xresult(xsoundex('Hanselmann'), '') == 'H-524')
    self.failUnless(xresult(xsoundex('Henzelmann'), '') == 'H-524')
    self.failUnless(xresult(xsoundex('Hildebrand'), '') == 'H-431')
    self.failUnless(xresult(xsoundex('Jackson'), '') == 'J-250')
    self.failUnless(xresult(xsoundex('Kavanagh'), '') == 'K-152')
    self.failUnless(xresult(xsoundex('Kuhne'), '') == 'K-500')
    self.failUnless(xresult(xsoundex('Lee'), '') == 'L-000')
    self.failUnless(xresult(xsoundex('Lind'), '') == 'L-530')
    self.failUnless(xresult(xsoundex('Lukaschowsky'), '') == 'L-222')
    self.failUnless(xresult(xsoundex('McDonnell'), '') == 'M-235')
    self.failUnless(xresult(xsoundex('McGee'), '') == 'M-200')
    self.failUnless(xresult(xsoundex('OBrien'), '') == 'O-165')
    self.failUnless(xresult(xsoundex('O\'Brien'), '') == 'O-165')
    self.failUnless(xresult(xsoundex('Opnian'), '') == 'O-155')
    self.failUnless(xresult(xsoundex('Oppenheimer'), '') == 'O-155')
    self.failUnless(xresult(xsoundex('Pfister'), '') == 'P-236')
    self.failUnless(xresult(xsoundex('Riedemanas'), '') == 'R-355')
    self.failUnless(xresult(xsoundex('Sa'), '') == 'S-000')
    self.failUnless(xresult(xsoundex('Schultz'), '') == 'S-432')
    self.failUnless(xresult(xsoundex('Shinka'), '') == 'S-520')
    self.failUnless(xresult(xsoundex('Sister'), '') == 'S-236')
    self.failUnless(xresult(xsoundex('Smith'), '') == 'S-530')
    self.failUnless(xresult(xsoundex('Smithe'), '') == 'S-530')
    self.failUnless(xresult(xsoundex('Smyth'), '') == 'S-530')
    self.failUnless(xresult(xsoundex('Smythe'), '') == 'S-530')
    self.failUnless(xresult(xsoundex('Tymczak'), '') == 'T-522')
    self.failUnless(xresult(xsoundex('VanDeusen'), '') == 'V-532')
    self.failUnless(xresult(xsoundex('Van Deusen'), '') == 'V-532')
    self.failUnless(xresult(xsoundex('VanDevanter'), '') == 'V-531')
    self.failUnless(xresult(xsoundex('Van Devanter'), '') == 'V-531')
    self.failUnless(xresult(xsoundex('Washington'), '') == 'W-252')
    self.failUnless(xresult(xsoundex('Wolves'), '') == 'W-412')
    self.failUnless(xresult(xsoundex('Zita'), '') == 'Z-300')
    self.failUnless(xresult(xsoundex('Zitzmeinn'), '') == 'Z-325')

if __name__ == '__main__':
  try:
    unittest.main()
  except SystemExit:
    pass
