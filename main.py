"""Module that runs self written 'C' language compiler for file 'source.c'

This compiler is written using 'rply' project 'https://github.com/alex/rply'
For proper work of my compiler you need to install 'rply' from github manually
because on PYPI there is older version.
"""

from compiler.astbuilder import ASTBuilder
from compiler.codegenerator import CodeGenerator


PATH_TO_SOURCE_FILE = 'source.c'

ast_builder = ASTBuilder(PATH_TO_SOURCE_FILE)
ast_builder.build_tree()
ast_builder.print_ast()

cg = CodeGenerator(ast_builder.parsed, asm_type='masm')
cg.write_to_file()
