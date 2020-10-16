from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union, Optional


class AbstractNode:
    """Abstract class for representing node of Abstract Syntax Tree

    All successors must include 'id_' attribute
    Can't initialize it here due to dataclass internal structure
    """

    def visit(self):
        pass


@dataclass
class Node(AbstractNode):
    """Represents node of Abstract Syntax Tree"""

    id_: str
    children: Optional[list, tuple] = field(default_factory=list)

    def add_children(self, children: Union[list, tuple]):
        self.children.extend(list(children))


@dataclass
class Function(AbstractNode):
    """Represents node of function with its arguments in AST"""

    name: str
    type_: str
    id_: str = 'function'
    arguments: Optional[list, tuple] = field(default_factory=list)
    body: Optional[list, tuple] = field(default_factory=list)

    def visit(self):
        for instruction in self.body:
            return instruction.visit()


@dataclass
class Return(AbstractNode):
    """Represents 'return' statement in AST"""

    expression: Union[Expression, int, float]
    id_: str = 'return'

    def visit(self):
        if isinstance(self.expression, Expression):
            return self.expression.visit()
        return self.expression


class Expression(AbstractNode):
    """Base class for unary and binary operations"""


@dataclass
class UnaryExpression(Expression):
    "Represents unary operation in 'C' language"

    value: Union[int, float]
    operator: str = '-'
    id_: str = 'unary_op'

    def visit(self):
        if self.operator == '-':
            code = [
                f'  mov eax, -{int(self.operand)}'
            ]
        return code


@dataclass
class BinaryExpression(Expression):
    "Represents binary operation in 'C' language"

    left_operand: UnaryExpression
    right_operand: UnaryExpression
    operator: str = '/'
    id_: str = 'binary_op'

    def visit(self):
        code = []
        if isinstance(self.left_operand, UnaryExpression):
            code.append(
                f'  mov eax, -{int(self.left_operand.value)}'
            )
        else:
            code.append(
                f'  mov eax, {int(self.left_operand)}'
            )
        code.append('  cdq')

        if isinstance(self.right_operand, UnaryExpression):
            code.append(
                f'  mov ebx, -{int(self.right_operand.value)}',
            )
        else:
            code.append(
                f'  mov ebx, {int(self.right_operand)}',
            )
        code.append('  cdq')

        code.append('\n  idiv ebx')
        return code
