import sys

def printError(*arg):
    print('Error:', *arg, file=sys.stderr)

def printDebug(*arg):
    print('Debug:', *arg, file=sys.stderr)

def printWarning(*arg):
    print('Warning:', *arg, file=sys.stderr)
