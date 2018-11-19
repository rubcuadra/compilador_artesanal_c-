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
	sw $a0, 4($sp)
	lw $a0, 4($sp)
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	
	.data
