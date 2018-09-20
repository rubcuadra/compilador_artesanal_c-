#Ruben Cuadra A01019102
from .globalTypes import * #Mandatory to have a TokenType.ENDFILE (Homework)
from .cMinusLexer import lexer

#Used to init programa global var
def globales(prog, pos, long):
    global programa
    programa = prog

def getToken(log=True): #We assume there is a global var called programa
    if lexer.lexdata is None: lexer.input(programa) # Give the lexer some input
    tok = lexer.token()
    if not tok or tok.value == TokenType.ENDFILE.value: return TokenType.ENDFILE, TokenType.ENDFILE.value #No hay mas, requisito del programa
    if log: print(f"{tok.type} => {tok.value}")
    return tok.type, tok.value #tok.type viene de la libreria, es diferente a TokenType

if __name__ == '__main__':
    f = open('../example.c-', 'r')
    programa = f.read() + TokenType.ENDFILE.value #Mandatory for the homework
    token, tokenString = getToken(True)
    while (token != TokenType.ENDFILE):
        token, tokenString = getToken(True)
