#Ruben Cuadra A01019102
if __name__ == '__main__':
	# Segundo Parcial
	from globalTypes import *
	from parser import parser, globales
	f = open('examples/3.c-', 'r')
	programa = f.read()
	progLong = len(programa)
	programa = programa + TokenType.ENDFILE.value
	posicion = 0
	
	globales(programa, posicion, progLong)
	AST = parser(False)