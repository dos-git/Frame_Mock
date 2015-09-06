__author__ = 'dos'

import unittest
import os, sys
import frame_mock as mock
from pprint import pprint

import inspect

# import tested module
import example_module
#test_module = __import__("example_module")


class Mock_Class_Example(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def printer(self, a, b):
        print "Method from mocked class"


#dummy_use - function used for to avoid information that some parameters
#            of mocked method or function were unused
#
def dummy_use(arg_1):
    _ = arg_1


class ExampleTestCase(unittest.TestCase):

    def setUp(self):
        #mock.list_mocked_method = []
        pass

    def tearDown(self):
        # restore mocked objects when tests are done
        for item in mock.list_mocked_method:
            item.restore()
            mock.list_mocked_method.remove(item)


    def test_replace_method(self):
        print "test_replace_method"

        # define mock that will be usd for a method replacement
        def mock_met(arg_1,arg_2, arg_3):
            print "Mock method was triggered."

        # replace method "printer" from the class "AA" of test_module
        mock.replace_method(example_module.AA, "printer", mock_met)

        a = example_module.AA("Domino", 5)
        a.printer("DOS", 5)

    def test_replace_class(self):
        print "test_replace_class"

        mock.replace_class(example_module, "AA", Mock_Class_Example)
        a = example_module.AA("", 5)
        a.printer("", 5)


    def test_replace_variable(self):
        print "test_replace_variable"

        mock_var = 5000
        mock.replace_item(example_module, "var", mock_var)
        print "NEW VAR %s" % example_module.var


    def test_replace_function(self):
        print "test_replace_function"

        def mock_fun():
            print "MOCK FUN!!!"

        mock.replace_item(example_module, "fun_for_fun", mock_fun)
        example_module.fun_for_fun()



if __name__ == "__main__":
    unittest.main()