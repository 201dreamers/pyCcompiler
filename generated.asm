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
  ahsl dd ?
  cchsl dd ?
  bhsl dd ?

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
  push ebx
  mov ebx, num2
  cmp num1, ebx
  je equal
  jne notequal
  equal:
    mov eax, 1
    jmp stop
  notequal:
    mov eax, 0
    jmp stop
  stop:
    pop ebx
    ret
  jmp stop
compare endp

ccchsl proc
  invoke divide, ahsl, 4
  push eax
  pop eax
  mov ahsl, eax
  invoke divide, ahsl, 4
  push eax
  pop eax
  mov ahsl, eax
  mov eax, ahsl
  push eax
  pop eax
  ret
ccchsl endp

main proc
  invoke divide, cchsl, bhsl
  push eax
  pop eax
  mov cchsl, eax
  invoke ccchsl
  pop eax
  mov bhsl, eax
  invoke divide, cchsl, bhsl
  push eax
  pop eax
  mov cchsl, eax
  invoke multiply, cchsl, 2
  push eax
  pop eax
  ret
main endp


end start