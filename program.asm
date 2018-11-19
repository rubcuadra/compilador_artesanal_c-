	.text
	.globl main
main:
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $a0, 2
	sw $a0, 28($sp)
	li $a0, 7
	sw $a0, 24($sp)
	li $a0, 0
	sw $a0, 20($sp)
	li $a0, 1
	sw $a0, 16($sp)
	li $a0, 2
	sw $a0, 12($sp)
	li $a0, 3
	sw $a0, 8($sp)
	li $a0, 4
	sw $a0, 4($sp)
	lw $a0, 4($sp)
	li $v0, 1
	syscall
	lw $a0, 8($sp)
	li $v0, 1
	syscall
	lw $a0, 12($sp)
	li $v0, 1
	syscall
	lw $a0, 16($sp)
	li $v0, 1
	syscall
	lw $a0, 20($sp)
	li $v0, 1
	syscall
	lw $a0, 24($sp)
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	
	.data
example:	.word 0
third:	.word 0
