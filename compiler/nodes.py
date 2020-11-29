from __future__ import annotations

from dataclasses import dataclass
from typing import Union, Optional, ClassVar, Literal

from compiler.miscellaneous import is_float


# class AbstractNode:
#     """Abstract class for representing node of Abstract Syntax Tree

#     All successors must include 'id_' attribute
#     Can't initialize it here due to dataclass internal structure
#     """
#     def visit(self):
#         pass


@dataclass(init=False)
class Program:
    """Represents node of function with its arguments in AST"""

    def __init__(self, contents: Union[list, tuple]):
        self.contents = contents
        self.id = 'program'

    def visit(self):
        asm_code = []
        for function in self.contents:
            if function is None:
                continue
            asm_code.extend(function.visit())

        return asm_code


@dataclass(init=False)
class Function:
    """Represents node of function with its arguments in AST"""

    all_functions: ClassVar[dict] = dict()
    SALT: ClassVar[str] = 'hsl'

    def __init__(self, name: str, type_: str,
                 arguments: Optional[Union[list, tuple]] = None,
                 body: Optional[Union[list, tuple]] = None):
        self.name = name
        self.type = type_
        self.id = 'function'
        self.arguments = arguments if arguments is not None else list()
        self.body = body if body is not None else list()
        self.name_with_salt = self.name if self.name == 'main'\
            else f'{self.name}{Function.SALT}'

        Function.all_functions[self.name] = self

    def visit(self):
        asm_code = [f'{self.name_with_salt} proc']
        for instruction in self.body:
            if instruction is None:
                continue
            asm_code.extend(instruction.visit())

        asm_code.extend((
            '  pop eax',
            '  ret',
            f'{self.name_with_salt} endp',
            ''
        ))

        return asm_code


@dataclass(init=False)
class Return:
    """Represents 'return' statement in AST"""

    def __init__(self, argument: Union[Expression, Variable, int, float]):
        self.argument = argument
        self.id = 'return'

    def visit(self):
        asm_code = []
        if isinstance(self.argument, Expression):
            return self.argument.visit()
        elif isinstance(self.argument, Variable):
            asm_code.append(f'  mov eax, {self.argument.name_with_salt}')
        elif is_float(self.argument):
            asm_code.append(f'  mov eax, {self.argument}')
        asm_code.append('  push eax')
        return asm_code


@dataclass(init=False)
class Variable:
    """Represents variable in 'C' language"""

    all_variables: ClassVar[dict] = dict()
    SALT: ClassVar[str] = 'hsl'

    def __init__(self, type_: Literal['int', 'float'], name: str,
                 expression:  Optional[Union[
                     UnaryExpression, BinaryExpression, int, float]] = None):
        self.type = type_
        self.name = name
        self.expression = expression
        self.id = 'variable'
        self.name_with_salt = f'{self.name}{Variable.SALT}'

        Variable.all_variables[self.name] = self

    @classmethod
    def generate_uninitialized_data_segment(cls):
        _uninitialized_data_segment = []
        for var in cls.all_variables.values():
            _uninitialized_data_segment.append(f'  {var.name_with_salt} dd ?')

        return _uninitialized_data_segment

    def visit(self):
        if self.expression is not None:
            asm_code = []
            if isinstance(self.expression, Expression):
                asm_code = self.expression.visit()
                asm_code.append('  pop eax')
                asm_code.append(f'  mov {self.name_with_salt}, eax')
            elif isinstance(self.expression, Variable):
                asm_code.extend((
                    f'  mov eax, {self.expression.name_with_salt}',
                    f'  mov {self.name_with_salt}, eax'
                ))
            else:
                asm_code.append(
                    f'  mov {self.name_with_salt}, {self.expression}')
        else:
            return []
        return asm_code


class Expression:
    """Base class for unary and binary operations"""

    __inactive_regs = ['eax', 'ebx', 'ecx', 'edx']
    __active_regs = []

    @classmethod
    def get_inactive_regs(cls):
        return cls.__inactive_regs.copy()

    @classmethod
    def get_active_regs(cls):
        return cls.__active_regs.copy()

    @classmethod
    def get_inactive_reg(cls):
        reg = cls.__inactive_regs.pop(0)
        cls.__active_regs.append(reg)
        return reg

    @classmethod
    def set_reg_active(cls, reg):
        if reg in cls.__inactive_regs:
            cls.__inactive_regs.remove(reg)
            cls.__active_regs.append(reg)

    @classmethod
    def set_reg_inactive(cls, reg):
        if reg in cls.__active_regs:
            cls.__inactive_regs.append(reg)
            cls.__active_regs.remove(reg)

    @classmethod
    def operand_is_zero(cls, operand):
        _is_zero = False
        if isinstance(operand, UnaryExpression):
            _is_zero = True if cls.operand_is_zero(operand.value) else False
        elif isinstance(operand, BinaryExpression):
            _is_zero = True if cls.operand_is_zero(operand.right_operand)\
                else False
        elif isinstance(operand, Variable):
            _is_zero = True if cls.operand_is_zero(operand.expression)\
                else False
        elif is_float(operand):
            _is_zero = True if operand == 0 else False

        return _is_zero

    @staticmethod
    def _process_operand(operand):
        asm_code = []
        if isinstance(operand, UnaryExpression):
            asm_code.extend(operand.visit())
            if isinstance(operand.value, Variable):
                operand_in_asm = operand.value.name_with_salt
            else:
                operand_in_asm = 'reg'
        elif isinstance(operand, BinaryExpression):
            asm_code.extend(operand.visit())
            operand_in_asm = 'reg'
        elif isinstance(operand, Variable):
            operand_in_asm = operand.name_with_salt
        else:
            operand_in_asm = f'{int(operand)}'

        return asm_code, operand_in_asm


@dataclass(init=False)
class FunctionCall(Expression):

    def __init__(
            self, function: Function, arguments: Union[list, tuple] = None):
        self.function = function
        self.arguments = arguments if arguments is not None else list()
        self.id = 'function_call'

    def visit(self):
        asm_code = []
        arguments_in_asm = []

        for argument in self.arguments:
            asm_code_of_argument, _argument_in_asm = \
                Expression._process_operand(argument)
            asm_code.extend(asm_code_of_argument)
            arguments_in_asm.appned(_argument_in_asm)

        for idx, argument in enumerate(arguments_in_asm):
            if argument == 'reg':
                reg = Expression.get_inactive_reg()
                asm_code.append(f'  pop {reg}')
                arguments_in_asm[idx] = reg
            elif is_float(self.value):
                reg = Expression.get_inactive_reg()
                asm_code.append(f'  mov {reg}, {int(self.value)}')
                arguments_in_asm[idx] = reg

        if arguments_in_asm:
            repr_of_arguments_in_asm = ', '.join(arguments_in_asm)
            asm_code.append(
                f'  invoke {self.function.name_with_salt}, '
                f'{repr_of_arguments_in_asm}'
            )
        else:
            asm_code.append(f'  invoke {self.function.name_with_salt}')

        for reg in Expression.get_active_regs():
            if reg in arguments_in_asm:
                Expression.set_reg_inactive(reg)

        Expression.set_reg_active('eax')

        return asm_code


@dataclass(init=False)
class UnaryExpression(Expression):
    """Represents unary operation in 'C' language"""

    def __init__(self, value: Union[int, float, Variable, Expression]):
        self.value: Union[int, float, Variable, Expression]
        self.operator = '-'
        self.id = 'unary_op'

    def visit(self):
        asm_code = []

        asm_code_of_expression,\
            operand_in_asm = Expression._process_operand(
                self.value)
        asm_code.extend(asm_code_of_expression)

        reg = Expression.get_inactive_reg()

        if operand_in_asm == 'reg':
            operand_in_asm = reg
            asm_code.append(f'  pop {operand_in_asm}')
        elif is_float(self.value):
            operand_in_asm = reg
            asm_code.append(f'  mov {operand_in_asm}, {int(self.value)}')

        asm_code.extend((
            f'  neg {operand_in_asm}',
            f'  push {operand_in_asm}'
        ))

        Expression.set_reg_inactive(reg)

        return asm_code


@dataclass(init=False)
class BinaryExpression(Expression):
    """Represents binary operation in 'C' language"""

    def __init__(self, left_operand: Union[Expression, Variable, int, float],
                 right_operand: Union[Expression, Variable, int, float],
                 operator: Literal['/', '*', '==']):
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.operator = operator
        self.id = 'binary_op'

    def visit(self):
        asm_code = []

        code_of_left_expression,\
            left_operand_in_asm = Expression._process_operand(
                self.left_operand)
        asm_code.extend(code_of_left_expression)

        code_of_right_expression,\
            right_operand_in_asm = Expression._process_operand(
                self.right_operand)
        asm_code.extend(code_of_right_expression)

        local_active_regs = []

        if left_operand_in_asm == 'reg' and right_operand_in_asm == 'reg':
            left_operand_in_asm = Expression.get_inactive_reg()
            right_operand_in_asm = Expression.get_inactive_reg()
            asm_code.extend(
                (f'  pop {right_operand_in_asm}',
                 f'  pop {left_operand_in_asm}')
            )
            local_active_regs.append(left_operand_in_asm)
            local_active_regs.append(right_operand_in_asm)
        elif left_operand_in_asm == 'reg':
            left_operand_in_asm = Expression.get_inactive_reg()
            asm_code.append(f'  pop {left_operand_in_asm}')
            local_active_regs.append(left_operand_in_asm)
        elif right_operand_in_asm == 'reg':
            right_operand_in_asm = Expression.get_inactive_reg()
            asm_code.append(f'  pop {right_operand_in_asm}')
            local_active_regs.append(right_operand_in_asm)

        if self.operator == '/':
            asm_code.append(
                ('  invoke divide, '
                 f'{left_operand_in_asm}, '
                 f'{right_operand_in_asm}')
            )
        elif self.operator == '*':
            asm_code.append(
                ('  invoke multiply, '
                 f'{left_operand_in_asm}, '
                 f'{right_operand_in_asm}')
            )
        elif self.operator == '==':
            asm_code.append(
                ('  invoke compare, '
                 f'{left_operand_in_asm}, '
                 f'{right_operand_in_asm}')
            )

        asm_code.append('  push eax')

        for reg in local_active_regs:
            Expression.set_reg_inactive(reg)

        Expression.set_reg_inactive('eax')

        return asm_code


@dataclass(init=False)
class TernaryExpression(Expression):
    """Represents binary operation in 'C' language"""

    DYNAMIC_SALT: ClassVar[int] = 0

    def __init__(self, condition: Union[Expression, Variable, int, float],
                 left_operand: Union[Expression, Variable, int, float],
                 right_operand: Union[Expression, Variable, int, float]):
        self.condition = condition
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.id = 'ternary_op'

    def visit(self):
        asm_code = []

        code_of_condition, condition_in_asm = \
            Expression._process_operand(self.condition)

        code_of_left_expression, left_operand_in_asm = \
            Expression._process_operand(self.left_operand)

        code_of_right_expression, right_operand_in_asm = \
            Expression._process_operand(self.right_operand)

        local_active_regs = []

        if condition_in_asm == 'reg':
            condition_in_asm = Expression.get_inactive_reg()
            code_of_condition.append(f'  pop {condition_in_asm}')
            local_active_regs.append(condition_in_asm)
        elif is_float(condition_in_asm):
            reg = Expression.get_inactive_reg()
            code_of_condition.append(f'  mov {reg}, {condition_in_asm}')
            condition_in_asm = reg
            local_active_regs.append(reg)

        if not code_of_left_expression:
            reg = Expression.get_inactive_reg()
            code_of_left_expression = (f'  mov {reg}, {left_operand_in_asm}',
                                       f'  push {reg}')
            Expression.set_reg_inactive(reg)

        if not code_of_right_expression:
            reg = Expression.get_inactive_reg()
            code_of_right_expression = (f'  mov {reg}, {right_operand_in_asm}',
                                        f'  push {reg}')
            Expression.set_reg_inactive(reg)

        indentation_separator = '\n  '

        asm_code.extend((
            *code_of_condition,
            f'  cmp {condition_in_asm}, 0',
            f'  je false{self.DYNAMIC_SALT}',
            f'  jne true{self.DYNAMIC_SALT}',
            f'  true{self.DYNAMIC_SALT}:',
            f'  {indentation_separator.join(code_of_left_expression)}',
            f'    jmp continue{self.DYNAMIC_SALT}',
            f'  false{self.DYNAMIC_SALT}:',
            f'  {indentation_separator.join(code_of_right_expression)}',
            f'    jmp continue{self.DYNAMIC_SALT}',
            '',
            f'  continue{self.DYNAMIC_SALT}:'
        ))

        for reg in local_active_regs:
            Expression.set_reg_inactive(reg)

        self.DYNAMIC_SALT += 1

        return asm_code
