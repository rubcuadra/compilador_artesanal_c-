from globalTypes import *
from lexer import getToken, globales

f = open('../example.c-', 'r')
programa = f.read() + TokenType.ENDFILE.value
progLong = len(programa) # longitud original del programa
posicion = 0
globales(programa, posicion, progLong)

# lee todo el archivo a compilar
# longitud original del programa
# agregar un caracter $ que represente EOF
# posición del caracter actual del string
token, tokenString = getToken(True)
while (token != TokenType.ENDFILE):
	token, tokenString = getToken(True)
	