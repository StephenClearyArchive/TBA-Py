#! /usr/bin/env python

# Copyright (C) 2001 Stephen Cleary (shammah@voyager.net)
# See the file 'COPYRIGHT' for copyright and disclaimer information

import os.path
from distutils.core import setup

setup(name = 'TBA',
      version = '1.0',
      description = 'General-Purpose Iterator Adapters',
      author = 'Stephen Cleary',
      author_email = 'shammah@voyager.net',
      url = 'http://sourceforge.net/projects/tba-py/',
      licence = "BSD-derived; see 'COPYRIGHT'",
      platforms = 'any',
      long_description = 'Useful pure Python modules',
      py_modules = [
                    'TBA.__init__',
                    'TBA.algorithms.__init__',
                    'TBA.algorithms.xbase',
                    'TBA.algorithms.xbasic',
                    'TBA.algorithms.xcompatibility',
                    'TBA.algorithms.xsorted',
                ],
      data_files = [
                    ('TBA',
                     [os.path.join('TBA', 'COPYRIGHT'),
                      os.path.join('TBA', 'README'),
                     ]),
                    (os.path.join('TBA', 'algorithms', 'test'),
                     [os.path.join('TBA', 'algorithms', 'test', 'test_xbasic.py'),
                      os.path.join('TBA', 'algorithms', 'test', 'test_xsorted.py'),
                     ]),
                    (os.path.join('TBA', 'algorithms', 'examples'),
                     [os.path.join('TBA', 'algorithms', 'examples', 'xsoundex.py'),
                     ]),
                    (os.path.join('TBA', 'algorithms', 'examples', 'test'),
                     [os.path.join('TBA', 'algorithms', 'examples', 'test', 'test_xsoundex.py'),
                     ]),
                   ],
)