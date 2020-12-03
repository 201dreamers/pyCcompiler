"""Module contains different misc functions"""

import sys


def is_number(obj):
    """Check if obj is number"""
    try:
        float(obj)
    except (ValueError, TypeError):
        return False
    return True


def exit_compiler(code: int = 0):
    """Stop program execution with message"""
    input("Program has finished. To exit press <Enter>\n")
    sys.exit(code)
