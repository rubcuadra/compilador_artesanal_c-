	li $gp 0
	addiu $gp $gp -4
	li $gp 0
	addiu $gp $gp -4
	li $gp 0
	addiu $gp $gp -4
function:
main:
	li $sp 0
	addiu $sp $sp -4
	li $sp 0
	addiu $sp $sp -4
	li $a0, 5
	sw $a0, 8($sp)
	li $a0, 3
	sw $a0, 12($gp)
	li $a0, 2
	sw $a0, 4($gp)
	sw $a0, 4($sp)
	li $v0, 1
	syscall
