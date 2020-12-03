from __future__ import annotations

from typing import Union, Optional, ClassVar, Literal

from compiler.miscellaneous import is_number


Register = Literal['eax', 'ebx', 'ecx', 'edx']
Operand = Union['Expression', 'Variable', int, float]


class Program:
    """Represents node of function with its arguments in AST"""

    __slots__ = ('id', 'contents')

    __all_functions = dict()
    __current_function_name: ClassVar[str] = None

    def __init__(self, contents: Union[list, tuple]):
        self.id: str = 'program'
        self.contents = contents

    @classmethod
    def add_function(cls, function: Function) -> None:
        cls.__all_functions[function.unique_key] = function

    @classmethod
    def get_function(cls, unique_key: str) -> Function | None:
        return cls.__all_functions.get(unique_key)

    @classmethod
    def get_functions(cls) -> dict:
        return cls.__all_functions.copy()

    @classmethod
    def get_current_function(cls) -> Function | None:
        return cls.__all_functions.get(cls.__current_function_name)

    @classmethod
    def set_current_function(cls, function_name: str) -> None:
        cls.__current_function_name = function_name

    @classmethod
    def generate_uninitialized_data_segment(cls) -> list:
        uninitialized_data_segment: list = list()
        for function in cls.__all_functions.values():
            for variable in function.get_variables().values():
                uninitialized_data_segment.append(
                    f'  {variable.name_with_salt} dd ?')

        return uninitialized_data_segment

    def generate_asm_code(self) -> list:
        asm_code = []
        for function in self.contents:
            if function is None:
                continue
            asm_code.extend(function.generate_asm_code())

        return asm_code

    def generate_ast_representation(self) -> str:
        contents = []
        for function in self.contents:
            if function is None:
                continue
            contents.append(
                function.generate_ast_representation())

        stringified_contents = ', '.join(contents)

        return f'{{"id":"{self.id}", "contents":[{stringified_contents}]}}'

    def __str__(self):
        return self.generate_ast_representation()


class Function:
    """Represents node of function with its arguments in AST"""

    __slots__ = ('id', 'name', 'type', 'arguments', 'body', 'name_with_salt',
                 'unique_key', '__all_variables')

    SALT: ClassVar[str] = 'hsl'

    def __init__(self, name: str, type_: str,
                 arguments: Union[list, tuple] = None,
                 body: Optional[Union[list, tuple]] = None):
        self.id = 'function'
        self.name = name
        self.type = type_
        self.arguments = arguments or list()
        self.body = body or list()
        self.unique_key = self.name

        if self.name == 'main':
            self.name_with_salt = self.name
        else:
            self.name_with_salt = f'{self.name}{Function.SALT}'

        self.__all_variables = dict()

        Program.add_function(self)
        Program.set_current_function(self.unique_key)

    def add_variable(self, variable: Variable) -> None:
        self.__all_variables[variable.name] = variable

    def get_variable(self, variable_name: str) -> Variable | None:
        return self.__all_variables.get(variable_name)

    def get_variables(self) -> dict:
        return self.__all_variables.copy()

    def variable_exists(self, variable_name: str) -> bool:
        return variable_name in self.__all_variables.keys()

    def generate_asm_code(self) -> list:
        asm_code = [f'{self.name_with_salt} proc']
        for instruction in self.body:
            if instruction is None:
                continue
            asm_code.extend(instruction.generate_asm_code())

        asm_code.extend((
            '  pop eax',
            '  ret',
            f'{self.name_with_salt} endp',
            ''
        ))

        return asm_code

    def generate_ast_representation(self) -> str:
        body = []
        for instruction in self.body:
            if instruction is None:
                continue
            body.append(instruction.generate_ast_representation())

        stringified_body = ', '.join(body)

        return (f'{{"id":"{self.id}", "name":"{self.name}",'
                f' "type":"{self.type}", "arguments":[],'
                f' "body":[{stringified_body}]}}')


class Return:
    """Represents 'return' statement in AST"""

    __slots__ = ('id', 'argument')

    def __init__(self, argument: Operand):
        self.id = 'return'
        self.argument = argument

    def generate_asm_code(self) -> list:
        asm_code = []
        if isinstance(self.argument, Expression):
            return self.argument.generate_asm_code()
        elif isinstance(self.argument, Variable):
            asm_code.append(f'  mov eax, {self.argument.name_with_salt}')
        elif is_number(self.argument):
            asm_code.append(f'  mov eax, {self.argument}')
        asm_code.append('  push eax')

        return asm_code

    def generate_ast_representation(self) -> str:
        if isinstance(self.argument, Expression):
            stringified_argument = self.argument.generate_ast_representation()
        elif isinstance(self.argument, Variable):
            stringified_argument = f'"{self.argument.name}"'
        else:
            stringified_argument = f'"{self.argument}"'

        return f'{{"id":"{self.id}", "argument":{stringified_argument}}}'


class Variable:
    """Represents variable in 'C' language"""

    __slots__ = ('id', 'type', 'name', 'name_with_salt', 'is_initialized')

    _SALT = 'hsl'

    def __init__(self, type_: Literal['int', 'float'], name: str):
        self.id = 'variable'
        self.type = type_
        self.name = name
        self.is_initialized = False
        self.name_with_salt = f'{self.name}{Variable._SALT}'
        Program.get_current_function().add_variable(self)

    def generate_ast_representation(self) -> str:
        if isinstance(self.expression, Expression):
            stringified_expression = \
                self.expression.generate_ast_representation()
        elif isinstance(self.expression, Variable):
            stringified_expression = f'"{self.expression.name}"'
        elif is_number(self.expression):
            stringified_expression = f'"{self.expression}"'
        else:
            stringified_expression = ""

        return (f'{{"id":"{self.id}", "type":{self.type},'
                f' "name":"{self.name}",'
                f' "expression":{stringified_expression}}}')


class VariableInitialization:

    __slots__ = ('id', 'name', 'type', 'expression', 'variable')

    def __init__(
        self, name: str, type_: Literal['int', 'float'] = None,
        expression: Optional[Union[Variable, Expression, int, float]] = None
    ):
        self.id = 'variable_assignment'
        self.name = name
        self.type = type_
        self.expression = expression
        self.variable = Program.get_current_function().get_variable(self.name)
        if self.variable is None and self.type is not None:
            self.variable = Variable(type_=self.type, name=self.name)
        self.variable.is_initialized = True

    def generate_asm_code(self) -> list:
        if self.expression is not None:
            asm_code = []
            if isinstance(self.expression, Expression):
                asm_code = self.expression.generate_asm_code()
                asm_code.append('  pop eax')
                asm_code.append(f'  mov {self.variable.name_with_salt}, eax')
            elif isinstance(self.expression, Variable):
                asm_code.extend((
                    f'  mov eax, {self.expression.name_with_salt}',
                    f'  mov {self.variable.name_with_salt}, eax'
                ))
            else:
                asm_code.append(
                    f'  mov {self.variable.name_with_salt}, {self.expression}')
        else:
            return []
        return asm_code

    def generate_ast_representation(self) -> str:
        if isinstance(self.expression, Expression):
            stringified_expression = \
                self.expression.generate_ast_representation()
        elif isinstance(self.expression, Variable):
            stringified_expression = f'"{self.expression.name}"'
        elif is_number(self.expression):
            stringified_expression = f'"{self.expression}"'
        else:
            stringified_expression = ""

        return (f'{{"id":"{self.id}", "name":"{self.name}",'
                f' "expression":{stringified_expression}}}')


class Expression:
    """Base class for unary and binary operations"""

    __inactive_regs = ['eax', 'ebx', 'ecx', 'edx']
    __active_regs = []

    @classmethod
    def get_inactive_regs(cls) -> list[str]:
        return cls.__inactive_regs.copy()

    @classmethod
    def get_active_regs(cls) -> list[str]:
        return cls.__active_regs.copy()

    @classmethod
    def get_inactive_reg(cls) -> Register:
        reg = cls.__inactive_regs.pop(0)
        cls.__active_regs.append(reg)
        return reg

    @classmethod
    def set_reg_active(cls, reg: Register) -> None:
        if reg in cls.__inactive_regs:
            cls.__inactive_regs.remove(reg)
            cls.__active_regs.append(reg)

    @classmethod
    def set_reg_inactive(cls, reg: Register) -> None:
        if reg in cls.__active_regs:
            cls.__inactive_regs.append(reg)
            cls.__active_regs.remove(reg)

    @classmethod
    def operand_is_zero(cls, operand: Operand) -> bool:
        is_zero = False
        if isinstance(operand, UnaryExpression):
            is_zero = True if cls.operand_is_zero(operand.value) else False
        elif isinstance(operand, BinaryExpression):
            is_zero = True if cls.operand_is_zero(operand.right_operand)\
                else False
        elif isinstance(operand, Variable):
            is_zero = True if cls.operand_is_zero(operand.expression)\
                else False
        elif is_number(operand):
            is_zero = True if operand == 0 else False

        return is_zero

    @staticmethod
    def _process_operand(operand) -> tuple[tuple, str]:
        asm_code = []
        if isinstance(operand, UnaryExpression):
            asm_code.extend(operand.generate_asm_code())
            if isinstance(operand.value, Variable):
                operand_in_asm = operand.value.name_with_salt
            else:
                operand_in_asm = 'reg'
        elif isinstance(operand, BinaryExpression):
            asm_code.extend(operand.generate_asm_code())
            operand_in_asm = 'reg'
        elif isinstance(operand, Variable):
            operand_in_asm = operand.name_with_salt
        elif isinstance(operand, FunctionCall):
            asm_code.extend(operand.generate_asm_code())
            operand_in_asm = 'eax'
        else:
            operand_in_asm = f'{int(operand)}'

        return tuple(asm_code), operand_in_asm


class FunctionCall(Expression):

    __slots__ = ('id', 'function_name', 'arguments', 'function')

    def __init__(self, function_name: str,
                 arguments: Union[list, tuple] = None):
        self.id = 'function_call'
        self.function_name = function_name
        self.arguments = arguments or list()

        # TODO: Rewrite function_name with unique_key
        self.function = Program.get_function(self.function_name)

    def generate_asm_code(self) -> list:
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
            elif is_number(self.value):
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

    def generate_ast_representation(self) -> str:
        return (f'{{"id":"{self.id}", "function_name":"{self.function_name}",'
                f' "arguments":[]}}')


class UnaryExpression(Expression):
    """Represents unary operation in 'C' language"""

    __slots__ = ('id', 'argument', 'operator')

    def __init__(self, argument: Union[int, float, Variable, Expression],
                 operator: str = '-'):
        self.id = 'unary_op'
        self.argument = argument
        self.operator = operator

    def generate_asm_code(self) -> list:
        asm_code = []

        asm_code_of_expression,\
            operand_in_asm = Expression._process_operand(
                self.value)
        asm_code.extend(asm_code_of_expression)

        reg = Expression.get_inactive_reg()

        if operand_in_asm == 'reg':
            operand_in_asm = reg
            asm_code.append(f'  pop {operand_in_asm}')
        elif is_number(self.value):
            operand_in_asm = reg
            asm_code.append(f'  mov {operand_in_asm}, {int(self.value)}')

        asm_code.extend((
            f'  neg {operand_in_asm}',
            f'  push {operand_in_asm}'
        ))

        Expression.set_reg_inactive(reg)

        return asm_code

    def generate_ast_representation(self) -> str:
        if isinstance(self.value, Expression):
            stringified_value = \
                self.value.generate_ast_representation()
        elif isinstance(self.value, Variable):
            stringified_value = f'"{self.value.name}"'
        elif is_number(self.value):
            stringified_value = f'"{self.value}"'
        else:
            stringified_value = ""

        return (f'{{"id":"{self.id}", "operator":"{self.operator}",'
                f' "value":{stringified_value}}}')


class BinaryExpression(Expression):
    """Represents binary operation in 'C' language"""

    __slots__ = ('id', 'left_operand', 'right_operand', 'operator')

    def __init__(self, left_operand: Operand, right_operand: Operand,
                 operator: Literal['/', '*', '==']):
        self.id = 'binary_op'
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.operator = operator

    def generate_asm_code(self) -> list:
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

    def generate_ast_representation(self) -> str:
        if isinstance(self.left_operand, Expression):
            stringified_left_operand = \
                self.left_operand.generate_ast_representation()
        elif isinstance(self.left_operand, Variable):
            stringified_left_operand = f'"{self.left_operand.name}"'
        elif is_number(self.left_operand):
            stringified_left_operand = f'"{self.left_operand}"'
        else:
            stringified_left_operand = ""

        if isinstance(self.right_operand, (Expression, Variable)):
            stringified_right_operand = \
                self.right_operand.generate_ast_representation()
        elif isinstance(self.right_operand, Variable):
            stringified_right_operand = f'"{self.right_operand.name}"'
        elif is_number(self.right_operand):
            stringified_right_operand = f'"{self.right_operand}"'
        else:
            stringified_right_operand = ""

        return (f'{{"id":"{self.id}", "operator":"{self.operator}",'
                f' "left_operand":{stringified_left_operand},'
                f' "right_operand":{stringified_right_operand}}}')


class TernaryExpression(Expression):
    """Represents binary operation in 'C' language"""

    __slots__ = ('id', 'left_operand', 'right_operand', 'condition')

    __DYNAMIC_SALT: ClassVar[int] = 0

    def __init__(self, left_operand: Operand, right_operand: Operand,
                 condition: Operand):
        self.id = 'ternary_op'
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.condition = condition

    def generate_asm_code(self) -> list:
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
        elif is_number(condition_in_asm):
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
            f'  je false{self.__DYNAMIC_SALT}',
            f'  jne true{self.__DYNAMIC_SALT}',
            f'  true{self.__DYNAMIC_SALT}:',
            f'  {indentation_separator.join(code_of_left_expression)}',
            f'    jmp continue{self.__DYNAMIC_SALT}',
            f'  false{self.__DYNAMIC_SALT}:',
            f'  {indentation_separator.join(code_of_right_expression)}',
            f'    jmp continue{self.__DYNAMIC_SALT}',
            '',
            f'  continue{self.__DYNAMIC_SALT}:'
        ))

        for reg in local_active_regs:
            Expression.set_reg_inactive(reg)

        self.__DYNAMIC_SALT += 1

        return asm_code

    def generate_ast_representation(self) -> str:
        if isinstance(self.left_operand, Expression):
            stringified_left_operand = \
                self.left_operand.generate_ast_representation()
        elif isinstance(self.right_operand, Variable):
            stringified_left_operand = f'"{self.left_operand.name}"'
        elif is_number(self.left_operand):
            stringified_left_operand = f'"{self.left_operand}"'
        else:
            stringified_left_operand = ""

        if isinstance(self.right_operand, Expression):
            stringified_right_operand = \
                self.right_operand.generate_ast_representation()
        elif isinstance(self.right_operand, Variable):
            stringified_right_operand = f'"{self.right_operand.name}"'
        elif is_number(self.right_operand):
            stringified_right_operand = f'"{self.right_operand}"'
        else:
            stringified_right_operand = ""

        return (f'{{"id":"{self.id}", "condition":"{self.condition}",'
                f' "left_operand":{stringified_left_operand},'
                f' "right_operand":{stringified_right_operand}}}')
