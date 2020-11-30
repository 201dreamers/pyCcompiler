from compiler.nodes import Variable


class CodeGenerator:
    """Class that creates assembly (masm) code from 'C' source code"""

    def __init__(self, program, output_file_name: str):
        self.program = program
        self.output_file_name = output_file_name
        self.procedures_from_source_code = None
        self.uninitialized_data_segment = None
        self.code_of_program = None

        self._initialize_masm()

    def _initialize_masm(self):
        header = (
            '.486',
            '.model flat, stdcall',
            'option casemap :none',
        )
        # TODO Add return_result procedure to masm
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

        division_procedure = (
            'divide proc num1:DWORD, num2:DWORD',
            '  mov eax, num1',
            '  cdq',
            '  idiv num2',
            '  ret',
            'divide endp'
        )

        multiplication_procedure = (
            'multiply proc num1:DWORD, num2:DWORD',
            '  mov eax, num1',
            '  cdq',
            '  imul num2',
            '  ret',
            'multiply endp'
        )

        comparison_procedure = (
            'compare proc num1:DWORD, num2:DWORD',
            '  push ebx',
            '  mov ebx, num2',
            '  cmp num1, ebx',
            '  je equal',
            '  jne notequal',
            '  equal:',
            '    mov eax, 1',
            '    jmp stop',
            '  notequal:',
            '    mov eax, 0',
            '    jmp stop',
            '  stop:',
            '    pop ebx',
            '    ret',
            '  jmp stop',
            'compare endp'
        )
        self.uninitialized_data_segment = tuple(
            Variable.generate_uninitialized_data_segment()
        )

        self.code_of_program = self.program.generate_asm_code()

        masm_code = (
            *header,
            '',
            *includes,
            '',
            '.data?',
            *self.uninitialized_data_segment,
            '',
            '.code',
            'start:',
            '  print chr$(13, 10, "-- Result of the source code --", 13, 10)',
            '  call main',
            '  print str$(eax)',
            '  print chr$(13, 10)',
            '  mov eax, input("To exit press <Enter>")',
            '  exit',
            '',
            *multiplication_procedure,
            '',
            *division_procedure,
            '',
            *comparison_procedure,
            '',
            *self.code_of_program,
            '',
            'end start'
        )

        self.generated_code = '\n'.join(masm_code)

    def write_to_file(self):
        with open(self.output_file_name, 'w')\
                as asm_file:
            asm_file.write(self.generated_code)
