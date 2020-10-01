"""Module contains different misc functions"""


def is_float(number):
    try:
        float(number)
    except ValueError:
        return False
    return True
