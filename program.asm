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
	li $a0, 6
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 1
	lw $t1 4($sp)
	add $a0 $t1 $a0
	addi $sp,$sp,4
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 3
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 5
	lw $t1 4($sp)
	mult $t1, $a0
	mflo $a0
	addi $sp,$sp,4
	lw $t1 4($sp)
	sub $a0 $t1 $a0
	addi $sp,$sp,4
	sw $a0, 4($sp)
	lw $a0, 4($sp)
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	
	.data
