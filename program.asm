	.text
	.globl main
main:
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $a0, 2
	sw $a0, 8($sp)
	li $a0, 3
	sw $a0, 4($sp)
	li $a0, 4
	la $a1, other
	sw $a0 0($a1)
	li $a0, 5
	la $a1, third
	sw $a0 0($a1)
	lw $a0, third
	li $v0, 1
	syscall
	lw $a0, other
	li $v0, 1
	syscall
	lw $a0, 4($sp)
	li $v0, 1
	syscall
	lw $a0, 8($sp)
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	
	.data
example:	.word 0
other:	.word 0
third:	.word 0
