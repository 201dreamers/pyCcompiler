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
  local var1hsl:DWORD
  local var2hsl:DWORD
  mov var1hsl, 16
  mov var2hsl, 18
  continue0:
  invoke divide, var1hsl, 2
  push eax
  pop eax
  mov var1hsl, eax
  jmp continue0
  invoke divide, var2hsl, 2
  push eax
  pop eax
  mov var2hsl, eax
  mov eax, 1
  cmp eax, 0
  je break0
  jne continue0
  break0:
  mov eax, var1hsl
  push eax
  pop eax
  ret
main endp


end start