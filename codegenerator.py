from astbuilder import ASTBuilder


class CodeGenerator:

    def __init__(self, node, asm_type: str = 'fasm'):
        self.return_value = self._walk_tree(node)
        self.asm_type = asm_type

        if self.asm_type == 'fasm':
            self._initialize_fasm()
        elif self.asm_type == 'masm':
            self._initialize_masm()

    def _initialize_fasm(self):
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

        self.generated_code = '\n'.join((
            self.header,
            self.start_func,
            self.exit_func
        ))

    def _initialize_masm(self):
        self.header = (
            '.386\n'
            '.model flat, stdcall\n'
            '.data\n'
            '.code\n'
        )

        self.main_proc = (
            'main PROC\n'
            f'\tmov eax, {self.return_value}\n'
            '\tret\n'
            'main ENDP\n'
        )

        self.start_func = (
            '_start:\n'
            '\tinvoke main\n'
            '\tinvoke ExitProcess, 0\n'
        )

        self.generated_code = '\n'.join((
            self.header,
            self.main_proc,
            self.start_func
        ))

    def _walk_tree(self, node):
        if node.id_ == 'function' and node.name == 'main':
            return self._walk_tree(node.children)
        elif node.id_ == 'return':
            return self._walk_tree(node.value)
        elif node.id_ == 'number':
            return node.value

    def write_to_file(self):
        with open(f'source_files/{self.asm_type}_generated.asm', 'w')\
                as asm_file:
            asm_file.write(self.generated_code)


if __name__ == "__main__":
    PATH_TO_SOURCE_FILE = 'source_files/source.c'

    ast_builder = ASTBuilder(PATH_TO_SOURCE_FILE)
    ast_builder.build_tree()

    cg = CodeGenerator(ast_builder.parsed, asm_type='masm')
    cg.write_to_file()
