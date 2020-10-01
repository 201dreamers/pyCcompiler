from astbuilder import ASTBuilder

from codegenerator import CodeGenerator


PATH_TO_SOURCE_FILE = 'source_files/source.c'

ast_builder = ASTBuilder(PATH_TO_SOURCE_FILE)
ast_builder.build_tree()

cg = CodeGenerator(ast_builder.parsed, asm_type='masm')
cg.write_to_file()
