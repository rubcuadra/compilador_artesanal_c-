from lexer import CMIN_Lexer

#Requisito
token  = None #Current
tokens = None #Generator

class ParserError(Exception):
    def __init__(self, message, token=None):
        super(ParserError, self).__init__(message)
        self.token = token

class Node:
    def __init__(self,_type,children=None,value=None,token=None):
        self.type  = _type
        self.value = value
        if children: self.children = children #Left,Right,blabla
        else:        self.children = [ ]
        self.token = token
    
    def __str__(self):
        return self.asString(self)

    def __repr__(self):
        return f"{self.type} {self.value}"
    
    def __getitem__(self,ix):
        return self.children[ix]

    @staticmethod
    def printTree(_node,level=0): #More efficient but it only prints
        if _node is None: return
        tb = (' |  '*level) + ' |- '
        print(f"{tb}{_node.type} {_node.value if _node.value!=None else ''}" )
        for c in _node.children:
            Node.printTree(c, level= level+1)

    @staticmethod
    def asString(_node,level=0): #Returns a String
        if _node is None: return ""
        tb = (' |  '*level) + ' |- '
        toRet = f"{tb}{_node.type} {_node.value if _node.value!=None else ''}\n"
        for c in _node.children: toRet += Node.asString(c, level= level+1)
        return toRet

def p_program(node_type="program"): #Returns root Node
    """program : declaration-list"""     
    return Node(node_type, children = p_declaration_list() ,token=token)

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
            return Node(node_type, [ts,decName], "VAR", token=token)
        elif match("LBRACK"):   # [
            cT = token
            iVal = Node(cT.type, value=cT.value,token=token) #INTEGER value
            if match("INTEGER") and match("RBRACK") and match("SEMI"):
                return Node(node_type, [ts,decName,Node("LBRACK"),iVal,Node("RBRACK") ], "ARRAY", token=token)
        elif match("LPAREN"):   # (
            params = p_params()
            if params and match("RPAREN"):
                cps = p_compound_stmt()
                if cps: #!=None
                    return Node(node_type, [ts,decName,*params,cps ], "FUNCTION", token=token)
    p_error()

def p_params(): #Returns a list of Nodes
    """
        params      : param_list 
                    | void
    """
    cT = token
    pl = p_param_list()
    if pl:                  return pl
    elif cT.type == "void": return [Node("void",token=token)] #Permitimos pl == None
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
        decName = Node(cT.type, value=cT.value,token=token)
        if match("LBRACK") and match("RBRACK"):
            return Node(node_type, [ts,decName,Node("LBRACK"),Node("RBRACK")], "ARRAY",token=token)
        else:
            return Node(node_type, [ts,decName], "VAR",token=token) 

def p_type_specifier():
    """
        type_specifier : int | void
    """
    if match("int") :  return Node("int",token=token)
    if match("void"):  return Node("void",token=token)

def p_compound_stmt(node_type="compound_statements"): #Returns a 
    """
        compound_stmt : { local_declarations_list statement_list }
    """
    if match("LCBRACES"):
        ldl = p_local_declarations_list()
        sl = p_statement_list()
        if match("RCBRACES"):
            return Node(node_type,[*ldl,*sl],token=token)
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
        p_return_stmt,
        p_expression_stmt,
        p_selection_stmt,
        p_iteration_stmt,
        p_compound_stmt
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
                    return Node("while",[e,s],token=token)
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
                        return Node("if",[e,s,s2],token=token) 
                return Node("if",[e,s],token=token) 
        p_error()

def p_return_stmt(node_type="return_stmt"):
    """
       return_stmt : return SEMI
                   | return expression SEMI 
    """
    if match("return"):
        if match("SEMI"):
            return Node(node_type,[Node("return"),Node("SEMI")],token=token)
        else:
            e = p_expression()
            if match("SEMI"):
                return Node(node_type,[Node("return"),e,Node("SEMI")],token=token)
            p_error()


def p_expression_stmt(node_type="expression_stmt"): #Can return None
    """
       expression_stmt : expression SEMI 
                       | SEMI 
    """
    if match("SEMI"):
        return Node("SEMI",token=token)
    else:
        e = p_expression()
        if e:
            if match("SEMI"): 
                return e 
            p_error()

def p_expression(node_type="expression",deb=False): 
    """
        expression : ID EQUALS expression 
                   | ID [ expression ] EQUALS expression
                   | ID [ expression ] {operations}  
                   | ID [ expression ] {operations} conditional {operations}
                   | factor {operations} 
                   | factor {operations} conditional {operations}
    """
    cT = token
    idNode = None
    if match("ID"): 
        idNode = Node(cT.type,value = cT.value,token=token)
        if match("EQUALS"):  #caso 1, asignar a una var
            return Node("EQUALS",[idNode,p_expression()],token=token)
        if match("LBRACK"):
            e = p_expression() #Node
            if match("RBRACK"):
                L = Node("ARRAY_POS",[idNode,Node("LBRACK"),e,Node("RBRACK")],token=token)
                if match("EQUALS"):
                    return Node("EQUALS",[L,p_expression()])
                else: 
                    idNode = L

        if match("LPAREN"): #CALL function, puede haber algo despues
            args = p_args()
            if match("RPAREN"):
                idNode = Node("CALL",[idNode]+args,token=token)

    factor = idNode if idNode else p_factor()
    factor = p_operations(factor) #Sacar multiplicaciones,divisiones,sumas,restas
    factor = p_conditionals(factor)
    return factor

def p_conditionals(factor):
    """
        conditional : relop factor 
    """
    relop = p_relop() #Checar si tiene relops
    if relop:
        R = p_factor()      #Obtener el factor de la derecha
        R = p_operations(R) #Sacar operaciones
        relop.children = [factor,R]
        return relop
    return factor

def p_operations(factor): #Create tree of operations and return it
    """
        operations : multis 
                   | multis sumres
                   | sumres
    """
    multis = p_multis(factor)
    sumres = p_sumres(multis) if multis else p_sumres(factor)
    sumres = sumres if sumres else multis #Caso si multis pero no sumres
    return sumres if sumres else factor 

def p_sumres(L): #Puede regresar None
    """
        sumres : { addop factor multis }
    """
    
    if L is None: L = Node("INTEGER",value=0,token=token) #For unitary +/-
    res = None
    addop = p_addop()
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
        if mulop is None: return L
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
        e = p_expression(deb=True)
        if match("RPAREN"):
            if e: return e #Node(node_type,[e],token=token)
            p_error()
        p_error()    
    else:
        cT = token
        if match("INTEGER"):     #NUM
            return Node(cT.type, value=cT.value,token=token) 
        if match("ID"):          #ID
            decName = Node(cT.type, value=cT.value,token=token) 
            if match("LBRACK"):  #ID [ expression ]
                e = p_expression()
                if match( "RBRACK" ): 
                    return Node("ARRAY_POS",[decName,Node("LBRACK"),e,Node("RBRACK")],token=token)
            
            elif match("LPAREN"): #CALL function
                args = p_args()
                if match("RPAREN"):
                    return Node("CALL",[decName]+args,token=token)
                p_error()
            return decName

def p_mulop(node_type="mulop"):
    if match("TIMES"):  return Node(node_type,[],"TIMES",token=token)
    if match("DIVIDE"): return Node(node_type,[],"DIVIDE",token=token)

def p_addop(node_type="addop"):
    if match("PLUS"):   return Node(node_type,[],"PLUS",token=token)
    if match("MINUS"):  return Node(node_type,[],"MINUS",token=token)

def p_relop(node_type="relop"):
    if match('LT'):     return Node(node_type,[],'LT',token=token)
    if match('LE'):     return Node(node_type,[],'LE',token=token)
    if match('GT'):     return Node(node_type,[],'GT',token=token)
    if match('GE'):     return Node(node_type,[],'GE',token=token)
    if match('EQ'):     return Node(node_type,[],'EQ',token=token)
    if match('NE'):     return Node(node_type,[],'NE',token=token)


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
            decName = Node(cT.type, value=cT.value,token=token)
            if match("SEMI"):     # ;
                return Node(node_type, [ts,decName], "VAR",token=token)
            elif match("LBRACK"):   # [
                cT = token
                iVal = Node(cT.type, value=cT.value,token=token) #INTEGER value
                if match("INTEGER") and match("RBRACK") and match("SEMI"):
                    return Node(node_type, [ts,decName,Node("LBRACK"),iVal,Node("RBRACK") ], "ARRAY",token=token)
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

def parser(imprime=True):
    if not programa: raise Exception("You should call 'globales' first")
    global tokens,token 
    lexer  = CMIN_Lexer(programa)
    tokens = lexer.tokensGenerator()
    token  = next(tokens)
    #Ya debe existir tokens y token
    result = p_program()
    if imprime:  Node.printTree(result) #print(result)
    return result
    
if __name__ == '__main__':
    #Segundo Parcial
    f = open('examples/0.c-', 'r')
    programa = f.read()
    programa = programa + '$' #Cuando quede hecho todo ver como remover el $
    globales(programa)
    AST = parser(True)
    