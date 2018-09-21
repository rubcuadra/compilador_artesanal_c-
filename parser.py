# def p_expression_binop(p):
#     '''expression : expression PLUS expression
#                   | expression MINUS expression
#                   | expression TIMES expression
#                   | expression DIVIDE expression'''
#     p[0] = Node("binop", [p[1],p[3]], p[2])
from cMinusLexer import lexer, eof_symbol
import traceback, sys

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

class ParserError(Exception):
    def __init__(self, message, token=None):
        super(ParserError, self).__init__(message)
        self.token = token

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
        print(f"{tb}{_node.type} {_node.value if _node.value!=None else ''}" )
        for c in _node.children:
            Node.printTree(c, level= level+1)

def p_program(node_type="program"): #Returns root Node
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

def p_declaration(node_type="declaration"): #Returns a Node
    """ declaration : type_specifier ID ; 
                    | type_specifier ID [ INTEGER ] ;
                    | type_specifier ID ( params ) compound-stmt"""
    ts = p_type_specifier() #Type of var
    cT = token              #ID value
    if match("ID"):
        decName = Node(cT.type, value=cT.value)
        if match("SEMI"):     # ;
            return Node(node_type, [ts,decName], "VARIABLE")
        elif match("LBRACK"):   # [
            cT = token
            iVal = Node(cT.type, value=cT.value) #INTEGER value
            if match("INTEGER") and match("RBRACK") and match("SEMI"):
                return Node(node_type, [ts,decName,Node("LBRACK"),iVal,Node("RBRACK") ], "ARRAY")
        elif match("LPAREN"):   # (
            params = p_params()
            if params and match("RPAREN"):
                cps = p_compound_stmt()
                if cps: #!=None
                    return Node(node_type, [ts,decName,*params,cps ], "FUNCTION")
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
    
def p_param(node_type="param"): #Can return None
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

def p_type_specifier():
    if match("int") :  return Node("int")
    if match("void"):  return Node("void")

def p_compound_stmt(node_type="compound_statements"): #Returns a 
    """
        compount_stmt : { local_declarations_list statement_list }
    """
    if match("LCBRACES"):
        ldl = p_local_declarations_list()
        sl = p_statement_list()
        if match("RCBRACES"):
            return Node(node_type,[*ldl,*sl])
    # p_error()

def p_local_declarations_list(node_type = "local_declaration"): #Returns array
    '''
        local_declarations_list : var_declarations local_declarations_list 
                                | empty
    '''
    nxt = p_var_declaration()
    ldl = []
    while nxt:
        ldl.append(nxt)
        nxt = p_var_declaration()
    return ldl

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
    return sl

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
        p_selection_stmt,
        p_iteration_stmt,
        p_compound_stmt,
        p_return_stmt
    ]
    for p in possibles:
        c = p()
        if c: return c

def p_iteration_stmt():
    """
        iteration_stmt : while ( expression ) statement
    """
    if match("while"):
        if match("LPAREN"):
            e = p_expression()
            
            for c in e.children: 
                if c == None: raise
                
            if e and match("RPAREN"):
                s = p_statement()
                if s:
                    return Node("while",[e,s])
        p_error()

def p_selection_stmt():
    """
        selection_stmt : if ( expression ) statement
                       | if ( expression ) statement else statement
    """
    if match("if"):
        if match("LPAREN"):
            e = p_expression() #Can't be None
            if e and match("RPAREN"):
                s = p_statement()
                if match("else"): #Segunda parte
                    s2 = p_statement()
                    if s2:
                        return Node("if",[e,s,s2]) 
                return Node("if",[e,s]) 
        p_error()

def p_return_stmt(node_type="return_stmt"):
    """
       return_stmt : return SEMI
                   | return expression SEMI 
    """
    if match("return"):
        if match("SEMI"):
            return Node(node_type,[Node("return"),Node("SEMI")])
        else:
            e = p_expression()
            if match("SEMI"):
                return Node(node_type,[Node("return"),e,Node("SEMI")])
            p_error()


def p_expression_stmt(node_type="expression_stmt"): #Can return None
    """
       expression_stmt : expression SEMI 
                       | SEMI 
    """
    if match("SEMI"):
        return Node("SEMI")
    else:
        e = p_expression()
        if e:
            if match("SEMI"): 
                return e 
            p_error()

def p_expression(node_type="expression"): 
    """
        expression : ID EQUALS expression 
                   | ID [ expression ] EQUALS expression
                   | ID [ expression ] multis sumres relop term sumres 
                   | ID [ expression ] sumres
                   | factor multis sumres relop term sumres
                   | factor multis sumres
    """
    cT = token
    idNode = None
    if match("ID"): 
        idNode = Node(cT.type,value = cT.value)
        if match("EQUALS"):  #caso 1, asignar a una var
            return Node("EQUALS",[idNode,p_expression()])
        if match("LBRACK"):
            e = p_expression() #Node
            if match("RBRACK"):
                L = Node("ARRAY_POS",[idNode,Node("LBRACK"),e,Node("RBRACK")])
                if match("EQUALS"):
                    return Node("EQUALS",[L,p_expression()])
                else: 
                    #Nodo de multiplicaciones
                    multis = p_multis(L) 
                    if multis:  #sumres relop term sumres 
                        sumres = p_sumres(multis)
                        if sumres:
                            relop = p_relop()
                            if relop:
                                term = p_factor()
                                sumres2 = p_sumres(term)
                                if sumres2: relop.children = [sumres,sumres2]
                                else:       relop.children = [sumres,term]
                                return relop
                            return sumres #SEGURO??
                        else:
                            relop = p_relop()
                            if relop:
                                term = p_factor()
                                sumres2 = p_sumres(term)
                                if sumres2: relop.children = [multis,sumres2]
                                else:       relop.children = [multis,term]
                                return relop
                            return multis #SEGURO??
                    else:   
                        sumres = p_sumres(L)
                        if sumres: 
                            relop = p_relop()
                            if relop:
                                term = p_factor()
                                sumres2 = p_sumres(term)
                                if sumres2: relop.children = [sumres,sumres2]
                                else:       relop.children = [sumres,term]
                                return relop
                            return sumres #SEGURO??
                        else:      
                            relop = p_relop()
                            if relop:
                                term = p_factor()
                                sumres2 = p_sumres(term)
                                if sumres2: relop.children = [multis,sumres2]
                                else:       relop.children = [multis,term]
                                return relop
                            return L
        if match("LPAREN"):
            args = p_args()
            if match("RPAREN"):
                return Node("CALL",[idNode]+args)

    factor = idNode if idNode else p_factor()
    multis = p_multis(factor)
    #AQUI HAY BUGGS

    if multis: #L es multis
        sumres = p_sumres(multis)
        relop = p_relop()
        if sumres: #L es sumres
            if relop:
                term2 = p_factor()
                sumres2 = p_sumres(term2)
                if sumres2: relop.children = [sumres,sumres2]
                else:       relop.children = [sumres,term2]
                return relop
            else: 
                return sumres
        else:  #L es multis
            if relop:
                term2 = p_factor()
                sumres2 = p_sumres(term2)
                if sumres2: relop.children = [multis,sumres2]
                else:       relop.children = [multis,term2]
                return relop
            else: 
                return multis
    else:      #L es factor
        sumres = p_sumres(factor)
        relop = p_relop()
        if sumres: #L is sumres
            if relop:
                term2 = p_factor()
                sumres2 = p_sumres(term2)
                if sumres2: relop.children = [sumres,sumres2]
                else:       relop.children = [sumres,term2]
                return relop
            else: 
                return sumres
        else: #L is factor
            if relop:
                term2 = p_factor()
                print(term2)
                sumres2 = p_sumres(term2)
                if sumres2: relop.children = [factor,sumres2]
                else:       relop.children = [factor,term2]
                return relop
            else: 
                return factor
    
def p_sumres(L): #Puede regresar None
    """
        sumres : { addop factor multis }
    """
    res = None
    addop = p_addop()
    if L is None: L = Node("INTEGER",value=0) #For unitary +/-
    while addop:
        addop.children = [L, p_factor()]
        mts = p_multis(addop)
        if mts: L = mts
        else:   L = addop
        res = L
        addop = p_addop()
    return res

def p_multis(L): #Puede regresar None
    """
        multis : { mulop factor }
    """
    mulop = p_mulop()    
    while mulop:
        mulop.children = [L, p_factor()] #p_factor no puede ser None
        L = mulop
        mulop = p_mulop()
    return mulop

def p_factor(node_type="factor"):
    """
        factor : ( expression )
               | NUM
               | ID
               | ID [ expression ]
               | ID ( args )
    """
    if match("LPAREN"):          #( expression )
        e = p_expression()
        if match("RPAREN"):
            if e: return Node(node_type,[Node("LPAREN"),e,Node("RPAREN")])
            return Node(node_type,[Node("LPAREN"),Node("RPAREN")])
        p_error()    
    else:
        cT = token
        if match("INTEGER"):     #NUM
            return Node(cT.type, value=cT.value) 
        if match("ID"):          #ID
            decName = Node(cT.type, value=cT.value) 
            if match("LBRACK"):  #ID [ expression ]
                e = p_expression()
                if match( "RBRACK" ): 
                    return Node(node_type,[decName,Node("LBRACK"),e,Node("RBRACK")])
            elif match("LPAREN"):#ID ( args )
                args = p_args()
                if match("RPAREN"):
                    return Node(node_type,[decName,Node("LPAREN"),*args,Node("RPAREN")])
                p_error()
            return decName

def p_mulop(node_type="mulop"):
    if match("TIMES"):  return Node(node_type,[],"TIMES")
    if match("DIVIDE"): return Node(node_type,[],"DIVIDE")

def p_addop(node_type="addop"):
    if match("PLUS"):   return Node(node_type,[],"PLUS")
    if match("MINUS"):  return Node(node_type,[],"MINUS")

def p_relop(node_type="addop"):
    if match('LT'):     return Node(node_type,[],'LT')
    if match('LE'):     return Node(node_type,[],'LE')
    if match('GT'):     return Node(node_type,[],'GT')
    if match('GE'):     return Node(node_type,[],'GE')
    if match('EQ'):     return Node(node_type,[],'EQ')
    if match('NE'):     return Node(node_type,[],'NE')


def p_args(): #Returns a list
    """
        args : expression { , expression }
             | empty
    """
    r = []
    e = p_expression()
    while e:
        r.append(e)
        if match("COMMA"): 
            e = p_expression()
            if not e: p_error()
        else: break
    return r

def p_var_declaration(node_type = "declaration"): #Can return None
    """ declaration : type_specifier ID ; 
                    | type_specifier ID [ INTEGER ] ;

        Similar to p_declaration but without functions and can return None
    """
    ts = p_type_specifier() #Type of var
    if ts:
        cT = token              #ID value
        if match("ID"):
            decName = Node(cT.type, value=cT.value)
            if match("SEMI"):     # ;
                return Node(node_type, [ts,decName], "VARIABLE")
            elif match("LBRACK"):   # [
                cT = token
                iVal = Node(cT.type, value=cT.value) #INTEGER value
                if match("INTEGER") and match("RBRACK") and match("SEMI"):
                    return Node(node_type, [ts,decName,Node("LBRACK"),iVal,Node("RBRACK") ], "ARRAY")
            else:
                p_error()
    

def p_error():
    print("ERROR ",token)
    raise ParserError("ERROR",token=token)

#Used to init programa global var
def globales(prog, pos=None, long=None):
    global programa
    programa = prog

def match(ttype):
    global token
    if ttype == token.type:
        # print(token)
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
    f = open('example2.c-', 'r')
    programa = f.read()
    programa = programa + '$' #Cuando quede hecho todo ver como remover el $
    globales(programa)
    AST = parse(True)
    

