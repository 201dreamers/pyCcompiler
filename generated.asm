.486
.model flat, stdcall
option casemap :none

include \masm32\include\windows.inc
include \masm32\macros\macros.asm
include \masm32\include\masm32.inc
include \masm32\include\gdi32.inc
include \masm32\include\user32.inc
include \masm32\include\kernel32.inc
include \masm32\include\msvcrt.inc
includelib \masm32\lib\masm32.lib
includelib \masm32\lib\gdi32.lib
includelib \masm32\lib\user32.lib
includelib \masm32\lib\kernel32.lib
includelib \masm32\lib\msvcrt.lib

.code
start:
  call main
  printf("\n-- Result of the source code --\n%d\n", eax)
  mov eax, input("To exit press <Enter>")
  exit

multiply proc num1:DWORD, num2:DWORD
  mov eax, num1
  cdq
  imul num2
  ret
multiply endp

divide proc num1:DWORD, num2:DWORD
  mov eax, num1
  cdq
  idiv num2
  ret
divide endp

summarize proc num1:DWORD, num2:DWORD
  mov eax, num1
  add eax, num2
  ret
summarize endp

subtract proc num1:DWORD, num2:DWORD
  mov eax, num1
  sub eax, num2
  ret
subtract endp

compare proc num1:DWORD, num2:DWORD
  mov eax, num2
  cmp num1, eax
  je equal
  jne notequal
  equal:
    mov eax, 1
    jmp stop
  notequal:
    mov eax, 0
    jmp stop
  stop:
    ret
  jmp stop
compare endp

lcompare proc num1:DWORD, num2:DWORD
  mov eax, num2
  cmp num1, eax
  jl less
  jge notless
  less:
    mov eax, 1
    jmp stop
  notless:
    mov eax, 0
    jmp stop
  stop:
    ret
  jmp stop
lcompare endp

logical_and proc num1:DWORD, num2:DWORD
  mov eax, num1
  cmp eax, 0
  je retfalse
  jne secondcheck
  secondcheck:
    mov eax, num2
    cmp eax, 0
    je retfalse
    jne rettrue
  rettrue:
    mov eax, 1
    jmp stop
  retfalse:
    mov eax, 0
    jmp stop
  stop:
    ret
  jmp stop
logical_and endp

logical_or proc num1:DWORD, num2:DWORD
  mov eax, num1
  cmp eax, 0
  je secondcheck
  jne rettrue
  secondcheck:
    mov eax, num2
    cmp eax, 0
    je retfalse
    jne rettrue
  rettrue:
    mov eax, 1
    jmp stop
  retfalse:
    mov eax, 0
    jmp stop
  stop:
    ret
  jmp stop
logical_or endp

fibb_recursionhsl proc nhsl:DWORD
  invoke lcompare, nhsl, 0
  push eax
  pop eax
  cmp eax, 0
  je false0
  jne true0
  true0:
    mov ebx, 0
    push ebx
    jmp continue0
  false0:
    mov ecx, nhsl
    push ecx
    jmp continue0

  continue0:
  pop eax
  mov nhsl, eax
  invoke lcompare, nhsl, 2
  push eax
  pop edx
  cmp edx, 0
  je false1
  jne true1
  true1:
    mov ebx, nhsl
    push ebx
    jmp continue1
  false1:
    invoke subtract, nhsl, 1
    push eax
    pop edx
    invoke fibb_recursionhsl, edx
    push eax
    invoke subtract, nhsl, 2
    push eax
    pop ebx
    invoke fibb_recursionhsl, ebx
    push eax
    pop eax
    pop ecx
    invoke summarize, ecx, eax
    push eax
    jmp continue1

  continue1:
  pop eax
  ret
fibb_recursionhsl endp

fibb_iterationhsl proc nhsl:DWORD
  local reshsl:DWORD
  local tmp1hsl:DWORD
  local tmp2hsl:DWORD
  local ihsl:DWORD
  mov reshsl, 0
  mov tmp1hsl, 0
  mov tmp2hsl, 1
  mov ihsl, 0
  continue2:
  invoke summarize, tmp1hsl, tmp2hsl
  push eax
  pop eax
  mov reshsl, eax
  mov eax, tmp2hsl
  mov tmp1hsl, eax
  mov eax, reshsl
  mov tmp2hsl, eax
  invoke summarize, ihsl, 1
  push eax
  pop eax
  mov ihsl, eax
  invoke subtract, nhsl, 1
  push eax
  pop ecx
  invoke lcompare, ihsl, ecx
  push eax
  pop eax
  cmp eax, 0
  je break2
  jne continue2
  break2:
  invoke lcompare, nhsl, 0
  push eax
  pop ebx
  cmp ebx, 0
  je false3
  jne true3
  true3:
    mov edx, 0
    push edx
    jmp continue3
  false3:
    mov ecx, reshsl
    push ecx
    jmp continue3

  continue3:
  pop eax
  mov reshsl, eax
  invoke compare, nhsl, 1
  push eax
  pop eax
  cmp eax, 0
  je false4
  jne true4
  true4:
    mov edx, 1
    push edx
    jmp continue4
  false4:
    mov ecx, reshsl
    push ecx
    jmp continue4

  continue4:
  pop eax
  mov reshsl, eax
  mov eax, reshsl
  push eax
  pop eax
  ret
fibb_iterationhsl endp

main proc 
  mov ebx, 6
  invoke fibb_iterationhsl, ebx
  push eax
  pop eax
  ret
main endp


end start