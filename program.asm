main:
	li $gp 0
	addiu $gp $gp -4
	li $gp 0
	addiu $gp $gp -4
	li $gp 0
	addiu $gp $gp -4
	li $sp 0
	addiu $sp $sp -4
	li $sp 0
	addiu $sp $sp -4
	li $a0, 2
	sw $a0, 8($sp)
	li $a0, 3
	sw $a0, 4($sp)
	li $a0, 4
	sw $a0, 8($gp)
	li $a0, 5
	sw $a0, 4($gp)
	lw $a0, 4($sp)
	li $v0, 1
	syscall
	li $v0, 10
	syscall
