class CodeGenerator:
    """Class that creates assembly (masm) code from 'C' source code"""

    def __init__(self, node, asm_type: str = 'fasm'):
        self.return_value = self._walk_tree(node)
        self.asm_type = asm_type

        if self.asm_type == 'fasm':
            self._initialize_fasm()
        elif self.asm_type == 'masm':
            self._initialize_masm()

    def _initialize_fasm(self):
        # TODO rewrite
        pass

    def _initialize_masm(self):
        self.header = (
            '.386\n'
            '.model flat, stdcall\n\n'
            'include \\masm32\\include\\kernel32.inc\n'
            'include \\masm32\\include\\user32.inc\n\n'
            'includelib \\masm32\\lib\\kernel32.lib\n'
            'includelib \\masm32\\lib\\user32.lib\n'
            '\n'
        )

        self.data_segment = (
            '.data\n'
            '\tCaption db "Hakman Dmytro IO-81 lab1", 0\n'
            f'\tText db "{"-" * 15} Result of'
            f' source program {"-" * 15}", 13, 10, '
            f'"{self.return_value}", 0\n'
            '\n'
        )

        self.code_segment = (
            '.code\n'
            'start:\n'
            '\tinvoke MessageBoxA, 0, ADDR Text, ADDR Caption, 0\n'
            '\tinvoke ExitProcess, 0\n'
            'end start'
        )

        self.generated_code = '\n'.join((
            self.header,
            self.data_segment,
            self.code_segment
        ))

    def _walk_tree(self, node):
        if node.id_ == 'function' and node.name == 'main':
            return self._walk_tree(node.body)
        elif node.id_ == 'return':
            return self._walk_tree(node.argument)
        elif node.id_ == 'number':
            return node.value

    def write_to_file(self):
        with open(f'1-3-Python-IO-81-Hakman.asm', 'w')\
                as asm_file:
            asm_file.write(self.generated_code)
