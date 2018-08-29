from ply import *

keywords = (
    'else', "if", "int", "return", "void", "while"
)

tokens = keywords + (
    'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'LPAREN', 'RPAREN', "LBRACK", "RBRACK", "LCBRACES", "RCBRACES",
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
    'COMMA', 'SEMI', 
    'INTEGER', 'FLOAT', 'STRING',
    'ID', 
    'NEWLINE',
    "ENDOFFILE",
    "CCODE_COMMENT"
)

t_ignore = " \t" #Whitespaces and tabs

def t_ID(t):
    r'[a-zA-Z][a-zA-Z]*'
    if t.value in keywords:
        t.type = t.value
    return t

t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_POWER = r'\^'

t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LCBRACES = r'\{'
t_RCBRACES = r'}'

t_COMMA = r'\,'
t_SEMI = r';'

t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING = r'\".*?\"'

eof_symbol = "$"
t_ENDOFFILE = r"\$"

def printError(lexer, errorDescription, errorVal):
    errorLine = (lexer.lexdata.split('\n')[lexer.lineno]).replace('\t',' ') #replace for better error printing
    
    print(f"ERROR: {errorDescription}\n{lexer.lineno}:{errorLine}\n{' '*(errorLine.find(errorVal)+len(str(lexer.lineno))+1)}^\n")

def t_INTEGER(t):
    r'\d+'
    if t.lexer.lexdata[t.lexpos+len(t.value)].isalpha(): # ID that starts with numbers
        printError(t.lexer, f"Wrong integer format", t.value[0])
    else:
        t.value = int(t.value)    
        return t

def t_CCODE_COMMENT(t):
    r'(/\*(.|\n)*?\*/)' #|(//.*)' #This part is for C++ or C
    pass

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    pass

def t_error(t):
    printError(t.lexer, f"Unkown character {t.value[0]}", t.value[0])
    t.lexer.skip(1)

lexer = lex.lex(debug=0)