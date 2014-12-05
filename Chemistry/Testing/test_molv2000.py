"""
Copyright (c) 2014 Dan Obermiller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

You should have received a copy of the MIT License along with this program.
If not, see <http://opensource.org/licenses/MIT>
"""

try:
    import cStringIO as IO
except ImportError:
    import StringIO as IO
finally:
    import itertools
    import os
    import tempfile
    import unittest
    
    from Chemistry import compounds
    from Chemistry.parsing.mol import molv2000 as mol


class test_MolV2000(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls): 
        cls.moldata = IO.StringIO(""" benzene
 ACD/Labs0812062058
 
  6  6  0  0  0  0  0  0  0  0  1 V2000
    1.9050   -0.7932    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.9050   -2.1232    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.7531   -0.1282    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.7531   -2.7882    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.3987   -0.7932    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.3987   -2.1232    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
  2  1  1  0  0  0  0
  3  1  2  0  0  0  0
  4  2  2  0  0  0  0
  5  3  1  0  0  0  0
  6  4  1  0  0  0  0
  6  5  2  0  0  0  0
 M  END
""")
        cls.parsed_molfile = mol.MolV2000(cls.moldata)
        cls.parsed_molfile.parse()
    
    @classmethod
    def tearDownClass(cls): pass    
    
    def setUp(self):
        pass
        
    def test_version(self):
        self.assertEqual(self.parsed_molfile.version, 'V2000')
        
    def test_header(self):
        map(self.assertEqual, (self.parsed_molfile.title,
                               self.parsed_molfile.info,
                               self.parsed_molfile.comments),
                              ('benzene', 'ACD/Labs0812062058', None))
        
    def test_counts(self):
        self.assertEqual(self.parsed_molfile.counts,
                         {'aaa': '6', 'xxx': '0', 'bbb': '6', 'sss': '0',
                          'mmm': '1', 'ppp': '0', 'lll': '0', 'vvvvvv': 'V2000',
                          'fff': '0', 'iii': '0', 'rrr': '0', 'ccc': '0'})
                         
        
    def test_atom_block(self):
        map(self.assertEqual, [self.parsed_molfile.atoms['a{}'.format(i)] 
                               for i in xrange(1, 7)],
                              ["1.9050   -0.7932    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0".split(),
                               "1.9050   -2.1232    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0".split(),
                               "0.7531   -0.1282    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0".split(),
                               "0.7531   -2.7882    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0".split(),
                               "-0.3987   -0.7932    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0".split(),
                               "-0.3987   -2.1232    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0".split()])
        
    def test_bond_block(self):
        map(self.assertEqual, [self.parsed_molfile.bonds['b{}'.format(i)] 
                               for i in xrange(1, 7)],
                              ["2  1  1  0  0  0  0".split(),
                               "3  1  2  0  0  0  0".split(),
                               "4  2  2  0  0  0  0".split(),
                               "5  3  1  0  0  0  0".split(),
                               "6  4  1  0  0  0  0".split(),
                               "6  5  2  0  0  0  0".split()])
        
    @unittest.expectedFailure
    def test_atom_list_block(self):
        self.assertEqual(self.parsed_molfile.atom_list, {})
        
    @unittest.expectedFailure
    def test_stext_block(self):
        self.assertEqual(self.parsed_molfile.stext, {})
        
    def test_properties_block(self):
        self.assertEqual(self.parsed_molfile.properties, {})
    
    def tearDown(self): pass
    
    @unittest.expectedFailure
    def test_to3000(self):
        self.fail("NYI")
        
    @unittest.expectedFailure
    def test_from3000(self):
        self.fail("NYI")


class test_MolV2000Builder(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls): pass
    
    @classmethod
    def tearDownClass(cls): pass    
    
    def setUp(self): pass
    
    def tearDown(self): pass
    
    
if __name__ == '__main__':
    import types
    import sys
    
                          
    test_classes_to_run = [value for key, value in globals().items()
                           if (isinstance(value, (type, types.ClassType)) and
                               issubclass(value, unittest.TestCase))]
                               
    loader = unittest.TestLoader()
    big_suite = unittest.TestSuite(loader.loadTestsFromTestCase(test_class) 
                                   for test_class in test_classes_to_run)
                                   
    runner = unittest.TextTestRunner(sys.stdout, verbosity=1)
    runner.run(big_suite)
