#Ruben Cuadra A01019102
from globalTypes import TokenType #Mandatory to have a TokenType.ENDFILE (Homework)
from cMinusLexer import lexer

class CMIN_Lexer():
    def __init__(self, program):
        super(CMIN_Lexer, self).__init__()
        lexer.input(programa)

    def getToken(self, log=True):
        tok = lexer.token()
        if not tok or tok.value == TokenType.ENDFILE.value: return TokenType.ENDFILE, TokenType.ENDFILE.value #No hay mas, requisito del programa
        if log: print(f"{tok.type} => {tok.value}")
        return tok.type, tok.value #tok.type viene de la libreria, es diferente a TokenType


if __name__ == '__main__':
    f = open('examples/3.c-', 'r')
    programa = f.read() + TokenType.ENDFILE.value #Mandatory for the homework
    l = CMIN_Lexer(programa)

    token, tokenString = l.getToken(True)
    while (token != TokenType.ENDFILE):
        token, tokenString = l.getToken(True)
    