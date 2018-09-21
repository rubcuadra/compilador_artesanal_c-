#Ruben Cuadra A01019102
from globalTypes import TokenType
from cMinusLexer import lexer, eof_symbol

class CMIN_Lexer():
    def __init__(self, program):
        super(CMIN_Lexer, self).__init__()
        self.program = program
        lexer.input(program)

    def getToken(self, log=True):
        tok = lexer.token()
        if tok in [None, eof_symbol]: return TokenType.ENDFILE, TokenType.ENDFILE.value #No hay mas, requisito del programa
        if log:                       print(f"{tok.type} => {tok.value}")
        return tok.type, tok.value #tok.type viene de la libreria, es diferente a TokenType

    def tokensGenerator(self):
        lexer.input(self.program)
        ret = lexer.token()
        while not ret in [None, eof_symbol]:
            yield ret
            ret = lexer.token()

if __name__ == '__main__':
    f = open('examples/3.c-', 'r')
    p = f.read() + TokenType.ENDFILE.value #Mandatory for the homework
    #Example 1
    l = CMIN_Lexer(p)
    token, tokenString = l.getToken(True)
    while (token != TokenType.ENDFILE):
        token, tokenString = l.getToken(True)
    #Example 2
    for token in l.tokensGenerator(): print(token)
    