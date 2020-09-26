from astbuilder import ASTBuilder


class CodeGenerator:

    def __init__(self, node):
        self.return_value = self._walk_tree(node)

        self.header = (
            'format ELF64\n'
            'public _start\n'
        )

        self.start_func = (
            '_start:\n'
            '\tcall exit\n'
        )

        self.exit_func = (
            'exit:\n'
            '\tmov rax, 1\n'
            f'\tmov rbx, {self.return_value}\n'
            '\tint 0x80\n'
        )

    def _walk_tree(self, node):
        if node.id_ == 'function' and node.name == 'main':
            return self._walk_tree(node.children)
        elif node.id_ == 'return':
            return self._walk_tree(node.value)
        elif node.id_ == 'number':
            return node.value

    def generate(self):
        with open('source_files/generated.asm', 'w') as asm_file:
            asm_file.write(
                '\n'.join((
                    self.header,
                    self.start_func,
                    self.exit_func
                ))
            )


if __name__ == "__main__":
    PATH_TO_SOURCE_FILE = 'source_files/source.c'

    ast_builder = ASTBuilder(PATH_TO_SOURCE_FILE)
    ast_builder.build_tree()

    cg = CodeGenerator(ast_builder.parsed)
    cg.generate()
