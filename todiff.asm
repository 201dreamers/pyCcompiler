.486                                    ; create 32 bit code
.model flat, stdcall                    ; 32 bit memory model
option casemap :none                    ; case sensitive
 
include \masm32\include\windows.inc     ; always first
include \masm32\macros\macros.asm       ; MASM support macros

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

.data
  itm0  dd 0


.code                       ; Tell MASM where the code starts
start:                          ; The CODE entry point to the program

    call main                   ; branch to the "main" procedure
    exit

main proc

    push edx
    push eax
    push ebx

    xor eax, eax
    xor edx, edx

    mov eax, 10
    cdq
    mov ebx, 2
    cdq

    idiv ebx

    print str$(eax)
    print chr$(13,10)
    print str$(edx)
    print chr$(13,10)

    pop ebx
    pop eax
    pop edx

    ret

main endp

end start                       ; Tell MASM where the program ends