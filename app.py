"""Module that runs self written 'C' language compiler for file 'source.c'

This compiler is written using 'rply' project 'https://github.com/alex/rply'
For proper work of my compiler you need to install 'rply' from github manually
because on PYPI there is older version.
"""

from compiler.compiler import Compiler
from config import PATH_TO_SOURCE_FILE, PATH_TO_OUTPUT_FILE


cmp = Compiler(PATH_TO_SOURCE_FILE, PATH_TO_OUTPUT_FILE)
cmp.compile()
cmp.print_abstract_syntax_tree()
input("\nProgram has finished. To exit press <Enter>\n")
