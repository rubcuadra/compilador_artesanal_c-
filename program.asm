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
	la $a1, other0
	sw $a0 0($a1)
	li $a0, 5
	la $a1, third
	sw $a0 0($a1)
	li $a0, 6
	la $a1, other4
	sw $a0 0($a1)
	lw $a0, other4
	li $v0, 1
	syscall
	lw $a0, third
	li $v0, 1
	syscall
	lw $a0, other0
	li $v0, 1
	syscall
	lw $a0, 8($sp)
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	
	.data
example:	.word 0
other0:	.word 0
other1:	.word 0
other2:	.word 0
other3:	.word 0
other4:	.word 0
third:	.word 0
