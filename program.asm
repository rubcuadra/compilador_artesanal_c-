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
	li $a0, 0
	move $t5, $a0
	li $a0, 0
	li $t1, 4
	mult $a0, $t1
	mflo $a0
	la $a1, fibonacci
	add $a1, $a1, $a0
	sw $t5, 0($a1)
	li $a0, 1
	move $t5, $a0
	li $a0, 1
	li $t1, 4
	mult $a0, $t1
	mflo $a0
	la $a1, fibonacci
	add $a1, $a1, $a0
	sw $t5, 0($a1)
	li $a0, 2
	sw $a0, 12($sp)
stwhile1:
	lw $a0, 12($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 10
	lw $t1 4($sp)
	addi $sp,$sp,4
	blt $t1, $a0, ifwhile1
	j endwhile1
ifwhile1:
	lw $a0, 12($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 1
	lw $t1 4($sp)
	sub $a0 $t1 $a0
	addi $sp,$sp,4
	la $a1, fibonacci
	li $t1, 4
	mult $a0, $t1
	mflo $a0
	add $a1, $a1, $a0
	lw $a0, 0($a1)
	sw $a0, 8($sp)
	lw $a0, 12($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 2
	lw $t1 4($sp)
	sub $a0 $t1 $a0
	addi $sp,$sp,4
	la $a1, fibonacci
	li $t1, 4
	mult $a0, $t1
	mflo $a0
	add $a1, $a1, $a0
	lw $a0, 0($a1)
	sw $a0, 4($sp)
	lw $a0, 8($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	lw $a0, 8($sp)
	lw $t1 4($sp)
	add $a0 $t1 $a0
	addi $sp,$sp,4
	move $t5, $a0
	lw $a0, 12($sp)
	li $t1, 4
	mult $a0, $t1
	mflo $a0
	la $a1, fibonacci
	add $a1, $a1, $a0
	sw $t5, 0($a1)
	lw $a0, 12($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 2
	lw $t1 4($sp)
	sub $a0 $t1 $a0
	addi $sp,$sp,4
	la $a1, fibonacci
	li $t1, 4
	mult $a0, $t1
	mflo $a0
	add $a1, $a1, $a0
	lw $a0, 0($a1)
	li $v0, 1
	syscall
	addi $a0, $0, 0xA
	addi $v0, $0, 0xB
	syscall
	lw $a0, 12($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 1
	lw $t1 4($sp)
	add $a0 $t1 $a0
	addi $sp,$sp,4
	sw $a0, 12($sp)
	j stwhile1
endwhile1:
	li $v0, 10
	syscall
	
	.data
fibonacci:	.word 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
