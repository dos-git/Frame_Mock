__author__ = 'dos'

import sys, os
import inspect


#list_mocked_method - collection of mocked items
list_mocked_method = []

#Mocked_Item - class defines object to keep details about mocked item
#
class Mocked_Item(object):

    def __init__(self, item_name):
        self.item_name = item_name

#collect_info - retrieves details about mocking procedure,
#
#   #module             - keeps an object reference
#   #name_orig_methode  - holds an original method name
#   #attr_orig_methode  - holds a reference to an original method
#   #name_mock_methode  - holds a mocked method name
#   #attr_orig_methode  - holds a reference to a mocked method
#
    def collect_info(self, *items_list):

        if len(items_list) == 5:
            self.module = items_list[0]
            self.name_orig_item = items_list[1]
            self.attr_orig_item = items_list[2]
            self.name_mock_item = items_list[3]
            self.attr_mock_item = items_list[4]
        else:
            print "Wrong usage of mocking function for item %s." % self.item_name
            sys.exit(0)

#restore - restores an original values before a mock procedure
#
    def restore(self):

        delattr(self.module, self.name_orig_item)
        setattr(self.module, self.name_orig_item, self.attr_orig_item)

#verification - process a class's object in order to get the list of methods
#               and fields.
#
def verification(class_object):

    # list of built in methods
    list_inbuilt_method = [ '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__',
                            '__hash__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
                            '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__' ]

    # structure is the dictionary for holding object definition
    structure = {}
    structure["methods"] = []
    structure["fields"] = []

    # iterate over list of valid attributes of object
    for item_attr in dir(class_object):
        # exclude built in methods
        if item_attr not in list_inbuilt_method:
            if is_method(class_object, item_attr):
                structure["methods"].append(item_attr)
            else:
                structure["fields"].append(item_attr)
        else:
            pass

    return structure

# #is_method - check if object has a given method
#
def is_method(obj, name):
    return hasattr(obj, name) and inspect.ismethod(getattr(obj, name))

# #replace_class - operator used for a class substitution, before replacement there is performed a check
#                  of structure for original and mocked class
#
def replace_class(module, orig_class_name, attr_mock_class):

    diff_text = ""
    mock_class_name = attr_mock_class.__name__
    attr_orig_class = getattr(module, orig_class_name)

    # get implementation details
    orig_dict = verification(attr_orig_class)
    mock_dict = verification(attr_mock_class)

    # examine differences
    diff_dict_methods = [x for x in orig_dict["methods"] if x not in mock_dict["methods"]]
    diff_dict_fields = [x for x in orig_dict["fields"] if x not in mock_dict["fields"]]

    text_result = ""

    if len(diff_dict_methods) == 0 and len(diff_dict_fields) == 0:

        obj_met = Mocked_Item(attr_orig_class.__name__)
        obj_met.collect_info(module, attr_orig_class.__name__, attr_orig_class,
                             attr_mock_class.__name__, attr_mock_class)
        list_mocked_method.append(obj_met)

        # do the class substitution
        delattr(module, attr_orig_class.__name__)
        setattr(module, attr_orig_class.__name__, attr_mock_class)
        return

    # check reasons of error
    if len(diff_dict_methods) != 0:
        diff_next = ""
        diff_text = "The original and mock class have different methods:\n"
        for k in diff_dict_methods:
            diff_next = "%s " % str(k)
            diff_text += diff_next
        text_result += diff_text + "\n"

    elif len(diff_dict_fields) != 0:
        diff_next = ""
        diff_text = "The original and mock class have different fields:\n"
        for k in diff_dict_fields:
            diff_next = "%s " % str(k)
            diff_text += diff_next
        text_result += diff_text + "\n"

    print text_result

#return_name_from_attribute - checks if passed attribute reference belong
#                             to object refrence and retrives refrence's name
#
#   #my_attr        - passed attribute reference
#   #object_attr    - object reference (module or class), defult value is a
#   #                 current module
#
def return_name_from_attribute(my_attr, object_attr=sys.modules[__name__]):

    res = None
    # iterate over object's attributes
    for k,v in object_attr.__dict__.iteritems():
        if my_attr is v:
            res = k
            break
    return res

#replace_method - operator used for a method replacement
#
def replace_method(module, original_method_name, attr_mock_method):

    mock_method_name = return_name_from_attribute(attr_mock_method)
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
    obj_met.collect_info(module, original_method_name, attr_orig_method, mock_method_name, attr_mock_method)
    list_mocked_method.append(obj_met)

    delattr(module, original_method_name)
    setattr(module, original_method_name, attr_mock_method)

#replace_item - operator used for a variable or function replacement
#
def replace_item(module, original_variable_name, attr_mock_variable):

    mock_variable_name = return_name_from_attribute(attr_mock_variable)
    attr_orig_variable = getattr(module, original_variable_name)

    obj_met = Mocked_Item(original_variable_name)
    obj_met.collect_info(module, original_variable_name, attr_orig_variable, mock_variable_name, attr_mock_variable)
    list_mocked_method.append(obj_met)

    delattr(module, original_variable_name)
    setattr(module, original_variable_name, attr_mock_variable)



#replace_class(module_source, "CLASS_NAME", Mock_Class)
#replace_method(module_source.CLASS_NAME, "Method_Name", Mock_Function)
#replace_item(module_source, "function", tool_func)

if __name__ == "__main__":
    pass