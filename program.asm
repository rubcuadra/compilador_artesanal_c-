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
	li $a0, 10
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
	move $t5, $a0
	lw $a0, 8($sp)
	li $t1, 4
	mult $a0, $t1
	mflo $a0
	la $a1, k
	add $a1, $a1, $a0
	sw $t5, 0($a1)
	lw $a0, 8($sp)
	la $a1, k
	li $t1, 4
	mult $a0, $t1
	mflo $a0
	add $a1, $a1, $a0
	lw $a0, 0($a1)
	sw $a0, 8($sp)
	j stwhile1
endwhile1:
	li $a0, 5
	la $a1, k
	li $t1, 4
	mult $a0, $t1
	mflo $a0
	add $a1, $a1, $a0
	lw $a0, 0($a1)
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	
	.data
k:	.word 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
