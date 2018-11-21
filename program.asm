	.text
	.globl main
sumar:
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $a0, 3
	sw $a0, 4($sp)
	lw $a0, 12($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	lw $a0, 12($sp)
	lw $t1 4($sp)
	add $a0 $t1 $a0
	addi $sp,$sp,4
	sw $a0 0($sp)
	addi $sp,$sp,-4
	lw $a0, 8($sp)
	lw $t1 4($sp)
	add $a0 $t1 $a0
	addi $sp,$sp,4
	addi $sp,$sp,4
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
#CALLING sumar
	lw $a0, 8($sp)
	addi $sp,$sp,-0
	sw $a0,0($sp)
	addi $sp,$sp, 0
	lw $a0, 4($sp)
	addi $sp,$sp,-4
	sw $a0,0($sp)
	addi $sp,$sp, 4
	addi $sp,$sp,-8
	jal sumar
	addi $sp,$sp,8
#FINISHED CALLING sumar
	sw $a0, 4($sp)
	lw $a0, 4($sp)
	li $v0, 1
	syscall
#CALLING sumar
	li $a0, 3
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 9
	lw $t1 4($sp)
	add $a0 $t1 $a0
	addi $sp,$sp,4
	addi $sp,$sp,-0
	sw $a0,0($sp)
	addi $sp,$sp, 0
	addi $sp,$sp,-4
	jal sumar
	addi $sp,$sp,4
#FINISHED CALLING sumar
	sw $a0, 4($sp)
	lw $a0, 4($sp)
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	
	.data
