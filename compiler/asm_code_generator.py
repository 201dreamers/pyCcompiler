class AsmCodeGenerator:
    """Class that creates assembly (masm) code from 'C' source code"""

    def __init__(self, program):
        self.program = program
        self.procedures_from_source_code = None

    def __initialize_masm(self):
        header = (
            '.486',
            '.model flat, stdcall',
            'option casemap :none',
        )

        # TODO?: Add return_result procedure to masm
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

        summarization_procedure = (
            'summarize proc num1:DWORD, num2:DWORD',
            '  mov eax, num1',
            '  add eax, num2',
            '  ret',
            'summarize endp'
        )

        subtraction_procedure = (
            'subtract proc num1:DWORD, num2:DWORD',
            '  mov eax, num1',
            '  sub eax, num2',
            '  ret',
            'subtract endp'
        )

        comparison_procedure = (
            'compare proc num1:DWORD, num2:DWORD',
            '  mov eax, num2',
            '  cmp num1, eax',
            '  je equal',
            '  jne notequal',
            '  equal:',
            '    mov eax, 1',
            '    jmp stop',
            '  notequal:',
            '    mov eax, 0',
            '    jmp stop',
            '  stop:',
            '    ret',
            '  jmp stop',
            'compare endp'
        )

        lcomparison_procedure = (
            'lcompare proc num1:DWORD, num2:DWORD',
            '  mov eax, num2',
            '  cmp num1, eax',
            '  jl less',
            '  jge notless',
            '  less:',
            '    mov eax, 1',
            '    jmp stop',
            '  notless:',
            '    mov eax, 0',
            '    jmp stop',
            '  stop:',
            '    ret',
            '  jmp stop',
            'lcompare endp'
        )

        logical_AND_procedure = (
            'logical_and proc num1:DWORD, num2:DWORD',
            '  mov eax, num1',
            '  cmp eax, 0',
            '  je retfalse',
            '  jne secondcheck',
            '  secondcheck:',
            '    mov eax, num2',
            '    cmp eax, 0',
            '    je retfalse',
            '    jne rettrue',
            '  rettrue:',
            '    mov eax, 1',
            '    jmp stop',
            '  retfalse:',
            '    mov eax, 0',
            '    jmp stop',
            '  stop:',
            '    ret',
            '  jmp stop',
            'logical_and endp'
        )

        logical_OR_procedure = (
            'logical_or proc num1:DWORD, num2:DWORD',
            '  mov eax, num1',
            '  cmp eax, 0',
            '  je secondcheck',
            '  jne rettrue',
            '  secondcheck:',
            '    mov eax, num2',
            '    cmp eax, 0',
            '    je retfalse',
            '    jne rettrue',
            '  rettrue:',
            '    mov eax, 1',
            '    jmp stop',
            '  retfalse:',
            '    mov eax, 0',
            '    jmp stop',
            '  stop:',
            '    ret',
            '  jmp stop',
            'logical_or endp'
        )

        code_of_program = self.program.generate_asm_code()

        masm_code = (
            *header,
            '',
            *includes,
            '',
            '.code',
            'start:',
            '  call main',
            r'  printf("\n-- Result of the source code --\n%d\n", eax)',
            '  mov eax, input("To exit press <Enter>")',
            '  exit',
            '',
            *multiplication_procedure,
            '',
            *division_procedure,
            '',
            *summarization_procedure,
            '',
            *subtraction_procedure,
            '',
            *comparison_procedure,
            '',
            *lcomparison_procedure,
            '',
            *logical_AND_procedure,
            '',
            *logical_OR_procedure,
            '',
            *code_of_program,
            '',
            'end start'
        )

        self.generated_code = '\n'.join(masm_code)

    def generate_asm_code(self, ):
        self.__initialize_masm()
        return self.generated_code
