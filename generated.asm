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
  chsl dd ?
  ahsl dd ?
  bhsl dd ?

.code
start:
  print chr$(13, 10, "-- Result of the source code --", 13, 10)
  call main
  print str$(eax)
  print chr$(13, 10)
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

main proc

  mov chsl, 2
  invoke compare, chsl, 2
  push eax
  pop eax
  cmp eax, 0
  je false35732
  jne true35732
  true35732:
    invoke compare, 2, 3
    push eax
    jmp continue35732
  false35732:
    invoke compare, 4, 1
    push eax
    jmp continue35732

  continue35732:
  pop eax
  mov ahsl, eax
  mov bhsl, 4
  invoke multiply, chsl, ahsl
  push eax

  pop eax

  ret
main endp
end start