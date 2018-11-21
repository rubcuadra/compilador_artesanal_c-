	.text
	.globl main
minloc:
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	lw $a0, 20($sp)
	sw $a0, 4($sp)
	lw $a0, 20($sp)
	mult $a0, 4
	mflo $a0
	sub $a0 24 $a0
	la $a1, x
	sw $a0 0($a1)
	lw $a0, 20($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 1
	lw $t1 4($sp)
	add $a0 $t1 $a0
	addi $sp,$sp,4
	sw $a0, 12($sp)
stwhile1:
	lw $a0, 12($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	lw $a0, 20($sp)
	lw $t1 4($sp)
	addi $sp,$sp,4
	blt $t1, $a0, ifwhile1
	j endwhile1
ifwhile1:
	lw $a0, 12($sp)
	mult $a0, 4
	mflo $a0
	sub $a0 24 $a0
	sw $a0 0($sp)
	addi $sp,$sp,-4
	lw $a0, x
	lw $t1 4($sp)
	addi $sp,$sp,4
	blt $t1, $a0, iftrue1
	j iffalse1
iftrue1:
	lw $a0, 12($sp)
	mult $a0, 4
	mflo $a0
	sub $a0 24 $a0
	la $a1, x
	sw $a0 0($a1)
	lw $a0, 12($sp)
	sw $a0, 4($sp)
	j ifcontinue1
iffalse1:
	li $a0, 3
	la $a1, x
	sw $a0 0($a1)
	li $a0, 3
	sw $a0 0($sp)
	addi $sp,$sp,-4
	lw $a0, x
	lw $t1 4($sp)
	mult $t1, $a0
	mflo $a0
	addi $sp,$sp,4
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 9
	lw $t1 4($sp)
	add $a0 $t1 $a0
	addi $sp,$sp,4
	sw $a0, 4($sp)
ifcontinue1:
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
	lw $a0, 4($sp)
	addi $sp,$sp,12
	jr $ra
sort:
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	lw $a0, 16($sp)
	sw $a0, 8($sp)
stwhile2:
	lw $a0, 8($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	lw $a0, 16($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 1
	lw $t1 4($sp)
	sub $a0 $t1 $a0
	addi $sp,$sp,4
	lw $t1 4($sp)
	addi $sp,$sp,4
	blt $t1, $a0, ifwhile2
	j endwhile2
ifwhile2:
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	lw $a0, 24($sp)
	addi $sp,$sp,-0
	sw $a0,0($sp)
	addi $sp,$sp, 0
	lw $a0, 12($sp)
	addi $sp,$sp,-4
	sw $a0,0($sp)
	addi $sp,$sp, 4
	lw $a0, 16($sp)
	addi $sp,$sp,-8
	sw $a0,0($sp)
	addi $sp,$sp, 8
	addi $sp,$sp,-12
	jal minloc
	addi $sp,$sp,12
	sw $a0, 8($sp)
	lw $a0, 8($sp)
	mult $a0, 4
	mflo $a0
	sub $a0 24 $a0
	sw $a0, 4($sp)
	lw $a0, 12($sp)
	mult $a0, 4
	mflo $a0
	sub $a0 24 $a0
	lw $a0, 8($sp)
	mult $a0, 4
	mflo $a0
	sub $a0 24 $a0
	lw $a0, 4($sp)
	lw $a0, 12($sp)
	mult $a0, 4
	mflo $a0
	sub $a0 24 $a0
	lw $a0, 12($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 1
	lw $t1 4($sp)
	add $a0 $t1 $a0
	addi $sp,$sp,4
	sw $a0, 12($sp)
	j stwhile2
endwhile2:
	addi $sp,$sp,12
	jr $ra
main:
	li $s0 0
	sw $s0,0($sp)
	addi $sp,$sp,-4
	li $a0, 0
	sw $a0, 4($sp)
stwhile3:
	lw $a0, 4($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 10
	lw $t1 4($sp)
	addi $sp,$sp,4
	blt $t1, $a0, ifwhile3
	j endwhile3
ifwhile3:
	li $v0, 5
	syscall
	move $a0, $v0
	la $a1, xi
	sw $a0 0($a1)
	lw $a0, 4($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 1
	lw $t1 4($sp)
	add $a0 $t1 $a0
	addi $sp,$sp,4
	sw $a0, 4($sp)
	j stwhile3
endwhile3:
	lw $a0, x
	addi $sp,$sp,-0
	sw $a0,0($sp)
	addi $sp,$sp, 0
	li $a0, 0
	addi $sp,$sp,-4
	sw $a0,0($sp)
	addi $sp,$sp, 4
	li $a0, 10
	addi $sp,$sp,-8
	sw $a0,0($sp)
	addi $sp,$sp, 8
	addi $sp,$sp,-12
	jal sort
	addi $sp,$sp,12
	li $a0, 0
	sw $a0, 4($sp)
stwhile4:
	lw $a0, 4($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 10
	lw $t1 4($sp)
	addi $sp,$sp,4
	blt $t1, $a0, ifwhile4
	j endwhile4
ifwhile4:
	lw $a0, xi
	li $v0, 1
	syscall
	lw $a0, 4($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 1
	lw $t1 4($sp)
	add $a0 $t1 $a0
	addi $sp,$sp,4
	sw $a0, 4($sp)
	j stwhile4
endwhile4:
	li $v0, 10
	syscall
	
	.data
z:	.word 0
x0:	.word 0
x1:	.word 0
x2:	.word 0
x3:	.word 0
x4:	.word 0
x5:	.word 0
x6:	.word 0
x7:	.word 0
x8:	.word 0
x9:	.word 0
