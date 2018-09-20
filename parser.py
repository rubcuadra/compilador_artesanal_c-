# def p_expression_binop(p):
#     '''expression : expression PLUS expression
#                   | expression MINUS expression
#                   | expression TIMES expression
#                   | expression DIVIDE expression'''
#     p[0] = Node("binop", [p[1],p[3]], p[2])
from cMinusLexer import lexer, eof_symbol

#Lexer
token  = None #Current
tokens = None #All
def TokensGenerator(program):
    lexer.input(program)
    ret = lexer.token()
    while not ret in [None, eof_symbol]:
        # print(f"{ret.type} => {ret.value}")
        yield ret
        ret = lexer.token()

class Node:
    def __init__(self,_type,children=None,value=None):
        self.type  = _type
        self.value = value
        if children: self.children = children #Left,Right,blabla
        else:        self.children = [ ]
    
    def __str__(self):
        return f"{self.type} {self.value}"
    
    @staticmethod
    def printTree(_node,level=0):
        if _node is None: return
        tb = (' |  '*level) + ' |- '
        print(f"{tb}{_node.type} {_node.value if _node.value else ''}" )
        for c in _node.children:
            Node.printTree(c, level= level+1)

def p_program(node_type="program"):
    """program : declaration-list"""     
    return Node(node_type, children = p_declaration_list() )

def p_declaration_list(): #Returns a list
    """
        declaration-list  : declaration declaration-list' 
        declaration-list' : declaration-list
                          | э
    """    
    if (token is None) or (token.type == "ENDOFFILE") : return []
    return [p_declaration()] + p_declaration_list()

def p_declaration(node_type="declaration"):
    """ declaration : type_specifier ID ; 
                    | type_specifier ID [ INTEGER ] ;
                    | type_specifier ID ( params ) compound-stmt"""
    ts = p_type_specifier() #Type of var
    cT = token              #ID value
    if match("ID"):
        decName = Node(cT.type, value=cT.value)
        if match("SEMI"):     # ;
            return Node(node_type, [ts,decName,Node("SEMI")], "VARIABLE")
        elif match("LBRACK"):   # [
            cT = token
            iVal = Node(cT.type, value=cT.value) #INTEGER value
            if match("INTEGER") and match("RBRACK") and match("SEMI"):
                return Node(node_type, [ts,decName,Node("LBRACK"),iVal,Node("RBRACK"),Node("SEMI") ], "ARRAY")
        elif match("LPAREN"):   # (
            params = p_params()
            if params and match("RPAREN"):
                cps = p_compount_stmt()
                if cps: #!=None
                    return Node(node_type, [ts,decName,Node("LPAREN"),*params,Node("RPAREN"),cps ], "FUNCTION")
    p_error()

def p_params(): #Returns a list of Nodes
    """
        params      : param_list 
                    | void
    """
    cT = token
    pl = p_param_list()
    if pl:                  return pl
    elif cT.type == "void": return [Node("void")] #Permitimos pl == None
    p_error()

def p_param_list(): #Returns a list of Nodes
    """
        param_list  : param param_list'
        param_list' : COMMA param_list
                    | э
    """
    p = [p_param()]
    
    if p[0]: #Not None
        while match("COMMA"): 
            p+=[p_param()]
        return p
    #Aqui no es error
    
def p_param(node_type="param"):
    """
        param       : type_specifier ID    
                    | type_specifier ID [ ]  
    """
    ts = p_type_specifier() #Type of var
    cT = token
    if match("ID"):
        decName = Node(cT.type, value=cT.value)
        if match("LBRACK") and match("RBRACK"):
            return Node(node_type, [ts,decName,Node("LBRACK"),Node("RBRACK")])
        else:
            return Node(node_type, [ts,decName]) 
    #Aqui no es error

def p_type_specifier():
    if match("int") :  return Node("int")
    if match("void"):  return Node("void")
    p_error()

def p_compount_stmt(node_type="compound_statements"):
    """
        compount_stmt : { local_declarations_list statement_list }
    """
    if match("LCBRACES"):
        ld = p_local_declarations_list()
        sl = p_statement_list()
        
        if match("RCBRACES"):
            return Node(node_type,[Node("LCBRACES"),*ld,*sl,Node("RCBRACES")])

    p_error()

def p_local_declarations_list(node_type = "local_declaration"): #Returns array
    '''
        local_declarations_list : var_declarations local_declarations_list 
                                | empty
    '''
    nxt = p_var_declaration()
    ld = []
    while nxt:
        ld.append(nxt)
        nxt = p_var_declaration()
    return ld

def p_statement_list(): #Returns array
    """
       statement_list :  statement statement_list
                      |  empty
    """
    nxt = p_statement()
    sl = []
    while nxt:
        sl.append(nxt)
        nxt = p_statement()
    return ld

def p_statement(): #Can return None
    """
        statement : expression_stmt
                  | compund_stmt
                  | selection_stmt
                  | iteration_stmt
                  | return_stmt
    """
    possibles = [
        p_expression_stmt,
        p_compount_stmt,
        p_selection_stmt,
        p_iteration_stmt,
        p_return_stmt
    ]
    for p in possibles:
        c = p()
        if c: return c

 
def p_var_declaration(node_type = "declaration"):
    """ declaration : type_specifier ID ; 
                    | type_specifier ID [ INTEGER ] ;

        Similar to p_declaration but without functions and can return None
    """
    ts = p_type_specifier() #Type of var
    cT = token              #ID value
    if match("ID"):
        decName = Node(cT.type, value=cT.value)
        if match("SEMI"):     # ;
            return Node(node_type, [ts,decName,Node("SEMI")], "VARIABLE")
        elif match("LBRACK"):   # [
            cT = token
            iVal = Node(cT.type, value=cT.value) #INTEGER value
            if match("INTEGER") and match("RBRACK") and match("SEMI"):
                return Node(node_type, [ts,decName,Node("LBRACK"),iVal,Node("RBRACK"),Node("SEMI") ], "ARRAY")
        else:
            p_error()
    #Can return None

def p_error():
    print("ERROR ",token)
    raise Exception("error")

#Used to init programa global var
def globales(prog, pos=None, long=None):
    global programa
    programa = prog

def match(ttype):
    global token
    if ttype == token.type:
        token = next(tokens) #Move to next token
        return True
    return False

def parse(imprime=True):
    if not programa: raise Exception("You should call 'globales' first")
    global tokens,token
    tokens = TokensGenerator(programa)
    token = next(tokens)
    #Ya debe existir tokens y token
    result = p_program()
    if imprime: Node.printTree(result)
    return result
    
if __name__ == '__main__':
    #Segundo Parcial
    f = open('example.c-', 'r')
    programa = f.read()
    programa = programa + '$' #Cuando quede hecho todo ver como remover el $
    globales(programa)
    AST = parse(True)
    

