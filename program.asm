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
	li $a0, 0
	sw $a0, 8($sp)
stwhile1:
	lw $a0, 8($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 5
	lw $t1 4($sp)
	addi $sp,$sp,4
	blt $t1, $a0, ifwhile1
	j endwhile1
ifwhile1:
	lw $a0, 8($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 1
	lw $t1 4($sp)
	add $a0 $t1 $a0
	addi $sp,$sp,4
	sw $a0, 8($sp)
	lw $a0, 8($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 2
	lw $t1 4($sp)
	mult $t1, $a0
	mflo $a0
	addi $sp,$sp,4
	move $t3, $a0
	lw $a0, 8($sp)
	la $a1, k
	li $t1, 4
	mult $a0, $t1
	mflo $a0
	add $a1, $a1, $a0
	sw $t3, 0($a1)
	lw $a0, 8($sp)
	la $a1, k
	li $t1, 4
	mult $a0, $t1
	mflo $a0
	add $a1, $a1, $a0
	lw $a0, 0($a1)
	li $v0, 1
	syscall
	j stwhile1
endwhile1:
	li $v0, 10
	syscall
	
	.data
k:	.word 0, 0, 0, 0, 0
