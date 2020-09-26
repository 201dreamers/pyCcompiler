from astbuilder import ASTBuilder

PATH_TO_SOURCE_FILE = 'source_files/source.c'

ast_builder = ASTBuilder(PATH_TO_SOURCE_FILE)
ast_builder.build_tree()
ast_builder.print_ast()
