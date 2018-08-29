from globalTypes import *
from lexer import getToken

f = open('../example.cminus', 'r')
programa = f.read() + TokenType.ENDFILE.value

# lee todo el archivo a compilar
# longitud original del programa
# agregar un caracter $ que represente EOF
# posición del caracter actual del string
token, tokenString = getToken(True)
while (token != TokenType.ENDFILE):
	token, tokenString = getToken(True)
	