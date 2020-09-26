format ELF64
public _start

_start:
	call exit

exit:
	mov rax, 1
	mov rbx, 4
	int 0x80
