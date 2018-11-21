	.text
	.globl main
sumar:
	li $a0, 3
	li $v0, 1
	syscall
	lw $a0, 8($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	lw $a0, 8($sp)
	lw $t1 4($sp)
	add $a0 $t1 $a0
	addi $sp,$sp,4
	addi $sp,$sp,0
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
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 2
	lw $t1 4($sp)
	addi $sp,$sp,4
	bge $a0, $t1, iftrue1
	j iffalse1
iftrue1:
	li $a0, 1
	li $v0, 1
	syscall
	j ifcontinue1
iffalse1:
	li $a0, 0
	li $v0, 1
	syscall
ifcontinue1:
	li $a0, 9
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	
	.data
