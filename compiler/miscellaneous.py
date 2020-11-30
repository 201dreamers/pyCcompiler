"""Module contains different misc functions"""

import sys


def is_float(number):
    try:
        float(number)
    except (ValueError, TypeError):
        return False
    return True


def exit_compiler(code: int = 0):
    input("Program has finished. To exit press <Enter>\n")
    sys.exit(code)


# class ProgramToASTConverter:

#     __slots__ = ('program_instance', 'dicted_program')

#     def __init__(self, program):
#         self.program_instance = program

#     def convert_to_dict(self):
#         self.dicted_program = self._asdict_for_dataclass_without_recursion(
#             self.program_instance)

#         contents = []
#         for func in self.dicted_program['contents']:
#             contents.append(self._asdict_for_dataclass_without_recursion(func))

#         self.dicted_program['contents'] = contents

#         for func in self.dicted_program['contents']:
#             body = []
#             for func_element in func['body']:
#                 print(f'\n{func_element}\n')
#                 p = self._asdict(func_element)
#                 body.append(p)
#                 print(f'\n{p=}\n')
#             func['body'] = body

#     def _asdict_for_dataclass_without_recursion(self, obj):
#         result = []
#         for f in fields(obj):
#             value = getattr(obj, f.name)
#             result.append((f.name, value))

#         return dict(result)

#     def _asdict(self, obj):
#         if is_dataclass(obj):
#             result = []
#             for f in fields(obj):
#                 value = self._asdict(getattr(obj, f.name))
#                 result.append((f.name, value))
#             return dict(result)
#         if isinstance(obj, (list, tuple)):
#             obj = tuple(obj)
#             return tuple(self._asdict(v) for v in (obj))
#         if isinstance(obj, dict):
#             return dict((k, self._asdict(v)) for k, v in obj.items())
#         return obj


# def to_dict(obj):
#     if is_dataclass(obj):
#         result = []
#         for f in fields(obj):
#             value = to_dict(getattr(obj, f.name))
#             result.append((f.name, value))
#         return dict(result)
#     if isinstance(obj, (list, tuple)):
#         obj = tuple(obj)
#         return tuple(to_dict(v) for v in (obj))
#     if isinstance(obj, dict):
#         return dict((k, to_dict(v)) for k, v in obj.items())
#     return obj
