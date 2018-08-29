#A01019102
#Utilice la implementación de variable estado o la de tabla. Recuerde que la implementación con variable estado es más eficiente.
from globalTypes import *
from cMinusLexer import lexer

def getToken(log=True):
    if lexer.lexdata is None: lexer.input(programa) # Give the lexer some input
    tok = lexer.token()
    if not tok or tok.value == TokenType.ENDFILE.value: return TokenType.ENDFILE, TokenType.ENDFILE.value #No hay mas, requisito del programa
    if log: print(f"{tok.type} => {tok.value}")
    return tok.type, tok.value #tok.type viene de la libreria, es diferente a TokenType

if __name__ == '__main__':
    f = open('../example.c-', 'r')
    
    programa = f.read() + TokenType.ENDFILE.value #Optional
    token, tokenString = getToken(True)
    while (token != TokenType.ENDFILE):
        token, tokenString = getToken(True)
