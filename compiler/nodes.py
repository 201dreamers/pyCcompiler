from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union, Optional


@dataclass
class AbstractNode:
    """Abstract class for representing node of Abstract Syntax Tree

    All successors must include 'id_' and 'children' attributes
    Can't assign it here due to dataclass internal structure
    """


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


@dataclass
class Return(AbstractNode):
    """Represents 'return' statement in AST"""

    argument: Number
    id_: str = 'return'


@dataclass
class Number(AbstractNode):
    """Represents number in AST"""
    value: Union[int, float]
    id_: str = 'number'
