"""Module contains different misc functions"""

import sys


def is_float(number):
    try:
        float(number)
    except ValueError:
        return False
    return True


def exit_compiler(code: int = 0):
    input("Program has finished. To exit press <Enter>")
    sys.exit(code)
