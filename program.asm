	.text
	.globl main
test:
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	lw $a0, 16($sp)
	sw $a0, 8($sp)
	addi $sp,$sp,8
	jr $ra
main:
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $a0, 2
	sw $a0, 8($sp)
	li $a0, 1
	sw $a0, 4($sp)
	lw $a0, 8($sp)
	lw $a0, 8($sp)
	sw $a0,0($sp)
	addi $sp,$sp,-4
	li $a0, 5
	lw $a0, 4($sp)
	sw $a0,0($sp)
	addi $sp,$sp,-4
	li $a0, 8
	lw $a0, 0($sp)
	sw $a0,0($sp)
	addi $sp,$sp,-4
	jal test
	addi $sp,$sp,4
	addi $sp,$sp,4
	addi $sp,$sp,4
	lw $a0, 4($sp)
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	
	.data
