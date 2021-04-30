	.section .data

strLOCK2:
	.asciz "Hello, World!\n"
	.section .bss
	.section .text
	.globl _start

_start:
	call main
	movl %eax, %ebx
	movl $1, %eax
	int $0x80

	.type main, @function
main:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl $5, %ecx
	movl %ecx, -4(%ebp)
	movl -4(%ebp), %ecx
	pushl %ecx
	movl $3, %ecx
	popl %edx
	cmpl %ecx, %edx
	jl .l1
	movl $strLOCK2, %ecx
	pushl %ecx
	call printf
	popl %ebx
	movl $9, %ecx
	pushl %ecx
	movl -4(%ebp), %ecx
	popl %edx
	addl %edx, %ecx
	pushl %ecx
	movl $5, %ecx
	pushl %ecx
	movl $9, %ecx
	popl %edx
	addl %edx, %ecx
	popl %edx
	cmpl %ecx, %edx
	jne .ne3
	movl $strLOCK2, %ecx
	pushl %ecx
	call printf
	popl %ebx
	.ne3:
	.l1:
	movl $9, %ecx
	movl %ecx, %eax
	jmp .leaver1
	.leaver1:
	movl %ebp, %esp
	popl %ebp
	ret
