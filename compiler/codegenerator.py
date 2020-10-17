class CodeGenerator:
    """Class that creates assembly (masm) code from 'C' source code"""

    def __init__(self, node, output_file_name: str):
        self.start_node = node
        self.output_file_name = output_file_name
        self.masm_code = None
        self.data_segment = []
        self.main_code = None

        self._initialize_masm()

    def _initialize_masm(self):
        self._walk_tree(self.start_node)

        header = (
            '.486',
            '.model flat, stdcall',
            'option casemap :none',
        )

        includes = (
            'include \\masm32\\include\\windows.inc',
            'include \\masm32\\macros\\macros.asm',
            'include \\masm32\\include\\masm32.inc',
            'include \\masm32\\include\\gdi32.inc',
            'include \\masm32\\include\\user32.inc',
            'include \\masm32\\include\\kernel32.inc',
            'include \\masm32\\include\\msvcrt.inc',
            'includelib \\masm32\\lib\\masm32.lib',
            'includelib \\masm32\\lib\\gdi32.lib',
            'includelib \\masm32\\lib\\user32.lib',
            'includelib \\masm32\\lib\\kernel32.lib',
            'includelib \\masm32\\lib\\msvcrt.lib',
        )

        division_proc = (
            'divide proc num1:DWORD, num2:DWORD',
            '  mov eax, num1',
            '  cdq',
            '  idiv num2',
            '  ret',
            'divide endp'
        )

        self.masm_code = (
            *header,
            '',
            *includes,
            '',
            '.data',
            *self.data_segment,
            '',
            '.code',
            'start:',
            '  print chr$("Hakman Dmytro IO-81 lab2", 13 ,10)',
            '  print chr$("--- Result of the source code ---", 13, 10)',
            '  call main',
            '  exit',
            '',
            *division_proc,
            '',
            'main proc',
            '  push eax',
            '  push ebx',
            '  push ecx',
            '  push edx',
            '',
            *self.main_code,
            '',
            '  print str$(eax)',
            '  print chr$(13, 10)',
            '',
            '  pop edx',
            '  pop ecx',
            '  pop ebx',
            '  pop eax',
            '',
            '  ret',
            'main endp',
            'end start'
        )

        self.generated_code = '\n'.join(self.masm_code)

    def _walk_tree(self, node):
        if node.id_ == 'function' and node.name == 'main':
            self.main_code = node.visit()

    def write_to_file(self):
        with open(self.output_file_name, 'w')\
                as asm_file:
            asm_file.write(self.generated_code)
