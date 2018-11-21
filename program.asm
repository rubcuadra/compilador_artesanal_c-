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
	li $a0, 1
	sw $a0, 4($sp)
stwhile1:
	lw $a0, 4($sp)
	sw $a0 0($sp)
	addi $sp,$sp,-4
	li $a0, 10
	lw $t1 4($sp)
	addi $sp,$sp,4
	blt $t1, $a0, ifwhile1
	j endwhile1
ifwhile1:
	lw $a0, 4($sp)
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
	j stwhile1
endwhile1:
	li $a0, 0
	li $v0, 1
	syscall
	li $v0, 10
	syscall
	
	.data
