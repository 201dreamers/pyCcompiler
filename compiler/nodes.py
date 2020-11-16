from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Union, Optional, ClassVar, Literal
from abc import ABC, abstractmethod

from compiler.miscellaneous import is_float


class AbstractNode(ABC):
    """Abstract class for representing node of Abstract Syntax Tree

    All successors must include 'id_' attribute
    Can't initialize it here due to dataclass internal structure
    """

    @abstractmethod
    def visit(self):
        pass


@dataclass
class Function(AbstractNode):
    """Represents node of function with its arguments in AST"""

    name: str
    type_: str
    id_: str = 'function'
    arguments: Optional[Union[list, tuple]] = field(default_factory=list)
    body: Optional[Union[list, tuple]] = field(default_factory=list)

    def visit(self):
        _asm_body_code = []
        for instruction in self.body:
            if instruction is None:
                continue
            _asm_body_code.extend(instruction.visit())

        return _asm_body_code


@dataclass
class Return(AbstractNode):
    """Represents 'return' statement in AST"""

    argument: Union[Expression, Variable, int, float]
    id_: str = 'return'

    def visit(self):
        _asm_code = []
        if isinstance(self.argument, Expression):
            return self.argument.visit()
        elif isinstance(self.argument, Variable):
            _asm_code.append(f'  mov eax, {self.argument.name_with_salt}')
        elif is_float(self.argument):
            _asm_code.append(f'  mov eax, {self.argument}')
        _asm_code.append('  push eax')
        return _asm_code


@dataclass
class Variable(AbstractNode):
    """Represents variable in 'C' language"""

    type_: Literal['int', 'float']
    name: str
    expression: Optional[
        Union[UnaryExpression, BinaryExpression, int, float]] = None
    id_: str = 'variable'
    all_variables: ClassVar[dict] = dict()
    SALT: ClassVar[str] = 'hsl'

    def __post_init__(self):
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
            _asm_code = []
            if isinstance(self.expression, Expression):
                _asm_code = self.expression.visit()
                _asm_code.append('  pop eax')
                _asm_code.append(f'  mov {self.name_with_salt}, eax')
            else:
                _asm_code.append(
                    f'  mov {self.name_with_salt}, {self.expression}')
        else:
            return []
        return _asm_code


class Expression(AbstractNode, ABC):
    """Base class for unary and binary operations"""

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
        _asm_code = []

        if isinstance(operand, UnaryExpression):
            _asm_code.extend(operand.visit())
            if isinstance(operand.value, Variable):
                operand_in_asm = operand.value.name_with_salt
            else:
                operand_in_asm = 'reg'
        elif isinstance(operand, BinaryExpression):
            _asm_code.extend(operand.visit())
            operand_in_asm = 'reg'
        elif isinstance(operand, Variable):
            operand_in_asm = operand.name_with_salt
        else:
            operand_in_asm = f'{int(operand)}'

        return _asm_code, operand_in_asm


@dataclass
class UnaryExpression(Expression):
    """Represents unary operation in 'C' language"""

    value: Union[int, float, Variable]
    operator: str = '-'
    id_: str = 'unary_op'

    def visit(self):
        _asm_code = []
        if isinstance(self.value, Variable):
            _asm_code.extend((
                f'  neg {self.value.name_with_salt}',
                f'  push {self.value.name_with_salt}'
            ))
        else:
            _asm_code.extend((
                f'  mov eax, {int(self.value)}',
                '  neg eax',
                '  push eax'
            ))
        return _asm_code


@dataclass
class BinaryExpression(Expression):
    """Represents binary operation in 'C' language"""

    left_operand: Union[UnaryExpression, Variable, int, float]
    right_operand: Union[UnaryExpression, Variable, int, float]
    operator: Literal['/', '*', '==']
    id_: str = 'binary_op'

    def visit(self):
        _asm_code = []

        code_of_left_expression,\
            left_operand_in_asm = Expression._process_operand(
                self.left_operand)
        _asm_code.extend(code_of_left_expression)

        code_of_right_expression,\
            right_operand_in_asm = Expression._process_operand(
                self.right_operand)
        _asm_code.extend(code_of_right_expression)

        if left_operand_in_asm == 'reg' and right_operand_in_asm == 'reg':
            _asm_code.extend(
                ('  pop ebx',
                 '  pop eax')
            )
            left_operand_in_asm = 'eax'
            right_operand_in_asm = 'ebx'
        elif left_operand_in_asm == 'reg':
            _asm_code.append('  pop eax')
            left_operand_in_asm = 'eax'
        elif right_operand_in_asm == 'reg':
            _asm_code.append('  pop eax')
            right_operand_in_asm = 'eax'

        if self.operator == '/':
            _asm_code.append(
                ('  invoke divide, '
                 f'{left_operand_in_asm}, '
                 f'{right_operand_in_asm}')
            )
            _asm_code.append('  push eax')
        elif self.operator == '*':
            _asm_code.append(
                ('  invoke multiply, '
                 f'{left_operand_in_asm}, '
                 f'{right_operand_in_asm}')
            )
            _asm_code.append('  push eax')
        elif self.operator == '==':
            _asm_code.append(
                ('  invoke compare, '
                 f'{left_operand_in_asm}, '
                 f'{right_operand_in_asm}')
            )
            _asm_code.append('  push eax')

        return _asm_code


@dataclass
class TernaryExpression(Expression):
    """Represents binary operation in 'C' language"""

    condition: Union[UnaryExpression, Variable, int, float]
    left_operand: Union[UnaryExpression, Variable, int, float]
    right_operand: Union[UnaryExpression, Variable, int, float]
    id_: str = 'ternary_op'

    def visit(self):
        _asm_code = []

        code_of_condition, condition_in_asm = \
            Expression._process_operand(self.condition)

        code_of_left_expression, left_operand_in_asm = \
            Expression._process_operand(self.left_operand)

        code_of_right_expression, right_operand_in_asm = \
            Expression._process_operand(self.right_operand)

        print()

        if condition_in_asm == 'reg':
            code_of_condition.append('  pop eax')
            condition_in_asm = 'eax'

        if not code_of_left_expression:
            code_of_left_expression = (f'  mov eax, {left_operand_in_asm}',
                                       '  push eax')

        if not code_of_right_expression:
            code_of_right_expression = (f'  mov eax, {right_operand_in_asm}',
                                        '  push eax')

        indentation_separator = '\n  '

        timestamp = time.monotonic_ns() % 100000
        _asm_code.extend((
            *code_of_condition,
            f'  cmp {condition_in_asm}, 0',
            f'  je false{timestamp}',
            f'  jne true{timestamp}',
            f'  true{timestamp}:',
            f'  {indentation_separator.join(code_of_left_expression)}',
            f'    jmp continue{timestamp}',
            f'  false{timestamp}:',
            f'  {indentation_separator.join(code_of_right_expression)}',
            f'    jmp continue{timestamp}',
            '',
            f'  continue{timestamp}:'
        ))

        return _asm_code
