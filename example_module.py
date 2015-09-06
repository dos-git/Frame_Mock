import os, sys

from pprint import pprint
var = 10000

def fun_for_fun():
    print "FUN VAR %d" % var


class AA(object):
    def __init__(self, n, v):
        self.name = n
        self.value = v
        self.value2 = v

    def printer(self, n2, v2):
        print self.name
        print self.value


if __name__ == "__main__":

    a = AA("DOMINO", 10)
    a.printer(" STEFANO", 99)

