__author__ = 'dos'

import sys, os
import inspect


def Verification(obj=object):

    # list of built in methods
    list_inbuilt_method = [ '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__',
                            '__hash__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
                            '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__' ]

    # structure is the dictionary for holding object definition
    structure = {}
    structure["methods"] = []
    structure["fields"] = []

    # iterate over list of valid attributes of object
    for i in dir(obj):
        if i not in list_inbuilt_method:
            if Is_Method(obj, i):
                structure["methods"].append(i)
            else:
                structure["fields"].append(i)
        else:
            pass

    return structure

# #Is_Method - check if object has a given method
#
def Is_Method(obj, name):
    return hasattr(obj, name) and inspect.ismethod(getattr(obj, name))

# #Replace_Class - operator used for a class substitution, before replacement there is performed a check
#                  of structure for original and mocked class
#
def Replace_Class(original_class, mock_class):

    diff_text = ""

    # get implementation details
    orig_dict = Verification(original_class)
    mock_dict = Verification(mock_class)

    # examine differences
    diff_dict_methods = [x for x in orig_dict["methods"] if x not in mock_dict["methods"]]
    diff_dict_fields = [x for x in orig_dict["fields"] if x not in mock_dict["fields"]]

    text_result = ""
    # do the class substitution
    if len(diff_dict_methods) == 0 and len(diff_dict_fields) == 0:
        print "replace"
        original_class = mock_class

        return

    # check reasons of error
    if len(diff_dict_methods) != 0:
        diff_next = ""
        diff_text = "The original and mock class have different methods:\n"
        for k in diff_dict_methods:
            diff_next = "%s " % str(k)
            diff_text += diff_next
        text_result += diff_text + "\n"

    if len(diff_dict_fields) != 0:
        diff_next = ""
        diff_text = "The original and mock class have different fields:\n"
        for k in diff_dict_fields:
            diff_next = "%s " % str(k)
            diff_text += diff_next
        text_result += diff_text + "\n"

    print text_result

# #Replace_Method - substitutes the original wit mocked method
#
def Replace_Method(module, method, mock_method):

    # get the attribute that represent method in a module
    at = getattr(module, method)
    original_fields =  inspect.getargspec(at)
    mock_fields =  inspect.getargspec(mock_method)


    diff_dict_methods = frozenset(original_fields).intersection(mock_fields)

    delattr(module, method)
    setattr(module, method, mock_method)


if __name__ == "__main__":

    pass