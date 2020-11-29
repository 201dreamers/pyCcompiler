"""Module contains different misc functions"""

import sys

from dataclasses import fields


def is_float(number):
    try:
        float(number)
    except (ValueError, TypeError):
        return False
    return True


def exit_compiler(code: int = 0):
    input("Program has finished. To exit press <Enter>\n")
    sys.exit(code)


def convert_to_dict(program_instance):
    result_dict = dict()
    result_list_of_tuples = list()
    for f in fields(program_instance):
        value = getattr(program_instance, f.name)
        result_list_of_tuples.append((f.name, value))

    return dict(result_list_of_tuples)
    # def inner_asdict(obj):



def to_dict(obj):
    if isinstance(obj, (list, tuple)):
        return tuple(to_dict(v, dict) for v in obj)
    elif isinstance(obj, dict):
        return dict((to_dict(k, dict), to_dict(v, dict))
                         for k, v in obj.items())
    else:
        result = []
        for f in fields(obj):
            value = to_dict(getattr(obj, f.name), dict)
            result.append((f.name, value))
        return dict(result)

# if isinstance(obj, (list, tuple)):
#     return type(obj)(to_dict(v, dict) for v in obj)
# elif isinstance(obj, dict):
#     return type(obj)((to_dict(k, dict),
#                     to_dict(v, dict))
#                     for k, v in obj.items())
# else:
#     result = []
#     for f in fields(obj):
#         value = to_dict(getattr(obj, f.name), dict)
#         result.append((f.name, value))
#     return dict(result)  
