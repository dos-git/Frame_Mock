__author__ = 'dos'

import sys, os
import inspect

sys.path.append("../Events")

import test2

#list_mocked_method - collection of mocked items
list_mocked_method = []

#Mocked_Item - class defines object to keep details about mocked item
#
class Mocked_Item(object):

    def __init__(self, item_name):
        self.item_name = item_name

#Collect_Info - retrieves details about mocking procedure,
#
#   #module             - keeps an object reference
#   #name_orig_methode  - holds an original method name
#   #attr_orig_methode  - holds a reference to an original method
#   #name_mock_methode  - holds a mocked method name
#   #attr_orig_methode  - holds a reference to a mocked method
#
    def Collect_Info(self, *items_list):

        if len(items_list) == 5:
            self.module = items_list[0]
            self.name_orig_method = items_list[1]
            self.attr_orig_method = items_list[2]
            self.name_mock_method = items_list[3]
            self.attr_mock_method = items_list[4]
        else:
            print "Wrong usage of mocking function for item %s." % self.item_name
            sys.exit(0)

#Restore - restores an original values before a mock procedure
#
    def Restore(self):
        delattr(self.module, self.name_orig_method)
        setattr(self.module, self.name_orig_method, self.attr_orig_method)

#Verification - process a class's object in order to get the list of methods
#               and fields.
#
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

#Return_Name_From_Attribute - checks if passed attribute reference belong
#                             to object refrence and retrives refrence's name
#
#   #my_attr        - passed attribute reference
#   #object_attr    - object reference (module or class), defult value is a
#   #                 current module
#
def Return_Name_From_Attribute(my_attr, object_attr=sys.modules[__name__]):

    res = None
    # iterate over object's attributes
    for k,v in object_attr.__dict__.iteritems():
        if my_attr is v:
            res = k
            break
    return res

#Replace_Method - operator used for a method replacement
#
def Replace_Method(module, original_method_name, attr_mock_method):

    mock_method_name = Return_Name_From_Attribute(attr_mock_method)
    attr_orig_method = getattr(module, original_method_name)
    original_fields =  inspect.getargspec(attr_orig_method)
    mock_fields =  inspect.getargspec(attr_mock_method)

    difference = len(original_fields.args) - len(mock_fields.args)

    if difference != 0:
        print "Cannot replace method because of parameters incompatibility."
        print "ORIGINAL METHOD: ", original_fields.args
        print "MOCK METHOD    : ", mock_fields.args
        sys.exit(0)

    obj_met = Mocked_Item(original_method_name)
    obj_met.Collect_Info(module, original_method_name, attr_orig_method, mock_method_name, attr_mock_method)
    list_mocked_method.append(obj_met)

    delattr(module, original_method_name)
    setattr(module, original_method_name, attr_mock_method)

#Replace_Variable - operator used for a variable replacement
#
def Replace_Variable(module, original_variable_name, attr_mock_variable):

    mock_variable_name = Return_Name_From_Attribute(attr_mock_variable)
    attr_orig_variable = getattr(module, original_variable_name)


    obj_met = Mocked_Item(original_variable_name)
    obj_met.Collect_Info(module, original_variable_name, attr_orig_variable, mock_variable_name, attr_mock_variable)
    list_mocked_method.append(obj_met)

    delattr(module, original_variable_name)
    setattr(module, original_variable_name, attr_mock_variable)



if __name__ == "__main__":

    pass

