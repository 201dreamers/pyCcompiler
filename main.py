"""Module that runs self written 'C' language compiler for file 'source.c'

This compiler is written using 'rply' project 'https://github.com/alex/rply'
For proper work of my compiler you need to install 'rply' from github manually
because on PYPI there is older version.
"""

from config import PATH_TO_SOURCE_FILE, PATH_TO_OUTPUT_FILE
from compiler.astbuilder import ASTBuilder
from compiler.codegenerator import CodeGenerator


ast_builder = ASTBuilder(PATH_TO_SOURCE_FILE)
ast_builder.build_tree()
ast_builder.print_ast()

cg = CodeGenerator(ast_builder.parsed, PATH_TO_OUTPUT_FILE)
cg.write_to_file()
input("\nProgram has finished. To exit press <Enter>")
