.386
.model flat, stdcall

include \masm32\include\kernel32.inc
include \masm32\include\user32.inc

includelib \masm32\lib\kernel32.lib
includelib \masm32\lib\user32.lib


.data
	Caption db "Hakman Dmytro IO-81 lab1", 0
	Text db "--------------- Result of source program ---------------", 13, 10, "0x11", 0


.code
start:
	invoke MessageBoxA, 0, ADDR Text, ADDR Caption, 0
	invoke ExitProcess, 0
end start