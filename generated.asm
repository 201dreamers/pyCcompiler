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

.data?

.code
start:
  print chr$(13, 10, "-- Result of the source code --", 13, 10)
  call main
  print str$(eax)
  print chr$(13, 10)
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

main proc 
  local chsl:DWORD
  local ahsl:DWORD
  local bhsl:DWORD
  mov chsl, 8
  mov bhsl, 1
  continue0:
  invoke divide, chsl, 2
  push eax
  pop eax
  mov chsl, eax
  invoke multiply, bhsl, 2
  push eax
  pop eax
  mov bhsl, eax
  invoke compare, chsl, 1
  push eax
  pop eax
  cmp eax, 0
  je false1
  jne true1
  true1:
    mov ebx, 0
    push ebx
    jmp continue1
  false1:
    mov ecx, 1
    push ecx
    jmp continue1

  continue1:
  pop eax
  mov ahsl, eax
  mov edx, 0
  cmp edx, 0
  je break0
  jne continue0
  break0:
  mov eax, bhsl
  push eax
  pop eax
  ret
main endp


end start