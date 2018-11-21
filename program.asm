	.text
	.globl main
update:
	lw $a0, 4($sp)
	move $t5, $a0
	lw $a0, 8($sp)
	li $t1, 4
	mult $a0, $t1
	mflo $a0
	lw $t1, 12($sp)
	sub $t1 $t1 $a0
	sw $t5, 0($t1)
	addi $sp,$sp,0
	jr $ra
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
	li $t1, 12
	add $sp,$sp,$t1
	move $a0, $sp
	sub $sp,$sp,$t1
	addi $sp,$sp,-0
	sw $a0,0($sp)
	addi $sp,$sp, 0
	li $a0, 2
	addi $sp,$sp,-4
	sw $a0,0($sp)
	addi $sp,$sp, 4
	li $a0, 10
	addi $sp,$sp,-8
	sw $a0,0($sp)
	addi $sp,$sp, 8
	addi $sp,$sp,-12
	jal update
	addi $sp,$sp,12
	li $a0, 2
	li $t1, 4
	mult $a0, $t1
	mflo $a0
	li $t2, 12
	sub $t1 $t2 $a0
	add $sp,$sp,$t1
	lw $a0, 0($sp)
	sub $sp,$sp,$t1
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	
	.data
k:	.word 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
