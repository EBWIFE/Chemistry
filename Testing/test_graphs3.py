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
    from collections import OrderedDict
    import graphs3 as Chemistry
    import contextlib
    import doctest
    import os
    import sys
    import unittest
    

@contextlib.contextmanager
def capture():
    oldout, olderr = sys.stdout, sys.stderr
    
    try:
        out=[IO.StringIO(), IO.StringIO()]
        sys.stdout, sys.stderr = out
        yield out
        
    finally:
        sys.stdout, sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()


class test_Compound(unittest.TestCase):
    
    def setUp(self): 
        self.compound1 = Chemistry.Compound(
                            {'a1':'H', 'a2':'H', 'a3':'O'}, 
                            {'b1':('a1', 'a2', {'order':1, 'chirality':None}), 
                             'b2':('a2', 'a3', {'order':1, 'chirality':None})})
    
    def tearDown(self): pass
    
    @classmethod
    def setUpClass(cls): pass
    
    @classmethod
    def tearDownClass(cls): pass
    
    def test__add_node_1(self): 
        self.assertRaises(KeyError,
                          self.compound1._add_node_,
                          *('a2', Chemistry.get_Element('H')))
                          
    def test__add_node_2(self): 
        self.compound1._add_node_('a4', Chemistry.get_Element('H'))
        self.assertIn('a4', self.compound1.nodes())
    
    def test__add_edge_1(self):
        self.assertRaises(KeyError,
                          self.compound1._add_edge_,
                          *('b3', 'a1', 'a2', {'order':1, 'chirality':None}))
    
    def test__add_edge_2(self):
        self.compound1._add_node_('a4', Chemistry.get_Element('H'))
        self.compound1._add_edge_('b1', 'a1', 'a4', 
                                  {'order':1, 'chirality':None})
        self.assertEqual(self.compound1['a1']['a4']['key'], "b1")
        

if __name__ == '__main__':
    import types
    
                          
    test_classes_to_run = []
    for key, value in globals().items():
        if isinstance(value, (type, types.ClassType)):
            if issubclass(value, unittest.TestCase):
                test_classes_to_run.append(value)

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)
    big_suite.addTests(doctest.DocTestSuite(Chemistry))

    runner = unittest.TextTestRunner(sys.stdout, verbosity=1)
    runner.run(big_suite)
