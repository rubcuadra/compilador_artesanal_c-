from enum import Enum

def error(node,msg):
    if node.token:raise Exception(f"ERROR LINE {node.token.lineno+1}, CHAR {node.token.lexpos+1} - {msg}")    
    else:         raise Exception(f"ERROR : {msg}")

class defTypes(Enum):
    ARR='array'
    VAR='variable'
    FUN='function'

class ScopeTree():
    def __init__(self,scope={},parent=None, tag=''):
        self.scope    = dict(scope) #Copy of Dict
        self.parent   = parent
        self.tag      = tag
        self.children = []
        self.depth    = None if parent else 0
    
    #dataType, strucType, value
    def addSymbol(self, s): 
        #Check if it already exists before inserting?
        if s.value == "ARRAY":
            self.scope[s.children[1].value] = (s.children[0].type,defTypes.ARR,s.children[3].value) 
            # for i in range( ch.children[3].value ): st.addSymbol(f'{ch.children[1].value}_{i}',ch.children[0].type) 
        elif s.value == "VAR":
            self.scope[s.children[1].value] = (s.children[0].type,defTypes.VAR,None) #Vars are initialized in None
        elif s.value == "FUNCTION":
            self.scope[s.children[1].value] = (s.children[0].type,defTypes.FUN,*s.children[2:-1]) #functions are initialized in None
        else: 
            error(s,"Wrong declaration")

    def getSymbol(self,var): 
        if var in self.scope: return self.scope[var]
        elif self.parent:     return self.parent.getSymbol(var)
        else:                 return None

    @staticmethod
    def appendChildren(root, parserNode):
        #Scope is created in this cases
        if parserNode.type == "declaration" and parserNode.value == "FUNCTION": 
            _scope = ScopeTree(parent=root,tag=parserNode.children[1].value)
            root.children.append(_scope)
            #Set params to this new scope
            for param in parserNode.children[2:-1]:
                if param.type == 'void': continue #Skip void in params
                _scope.addSymbol(param)
            #It just validates everything is fine, otherwise it raises exceptions
            validateCompoundStatements(parserNode[-1],_scope)
        else:
            error(parserNode,"Wrong declaration")

    def __str__(self): 
        return self.getStr(level=self.getDepth())

    def getDepth(self):
        if   self.depth:  return self.depth
        elif self.parent: self.depth = 1+self.parent.getDepth()
        return            self.depth

    def getStr(self, level=0):
        s = ""
        if self.parent: s += self.parent.getStr(level-1)
        s += '\t'*level
        s += f"{self.tag}\n"
        for key,val in self.scope.items():
            s += '\t'*(level+1)
            s += f"{val[0]} {key} - {val[1].value}\n"
        return s+'\n'

    #Goes to a leaf and prints the scope
    def printAllScopes(self):
        if self.children:
            for ch in self.children:
                ch.printAllScopes()
        else:
            print(self)

#Another block - IF/ELSE/WHILE/Function after declarations
def validateCompoundStatements(statementBlock, _scope): 
    if statementBlock.type == 'return_stmt':
        syb = _scope.getSymbol(_scope.tag)
        if syb[0] == getType(statementBlock[1],_scope): return
        else: error(statementBlock,f"Wrong return type on function {_scope.tag}")
    elif statementBlock.type != 'compound_statements': error(statementBlock,"Not a statement block ")
    #Body -> compound_statements
    for statement in statementBlock.children: 
        if statement.type == 'declaration': #Define it in the scope
            _scope.addSymbol(statement)
        elif statement.type == "EQUALS":    #Validate var exist and check that assign is of the same type
            if statement[0].type in ["ARRAY_POS", "ID"]:
                s = getType(statement[0],_scope)
                gt = getType(statement[1],_scope)
                if s == gt and s!=None: continue
                error(statement,f"Wrong data type assignment: {s[0]} {statement[0].value} => {gt}")
            else:
                error(statement,"Wrong assignment")
        elif statement.type == "CALL":      #Check called func exists and it is void
            s = getType(statement[0],_scope)
            if not s:     error(statement,f"Calling function without definition '{statement[0].value}'")
            if s!='void': error(statement,f"Called NON void function without assignment")
        elif statement.type == "return_stmt":  #Check returns exist
            s = _scope.getSymbol(_scope.tag) #SI es None es que we fucked up algo
            if s[0] == 'void' and len(statement.children)>1: error(statement,"ERROR: void function returning values")
            t = getType(statement[1],_scope)
            if s[0] == t: continue
            error(statement,f"Wrong return type {s[0]} != {t}")
        elif statement.type == "while":
            #We can only compare between ints
            if getType(statement[0],_scope) =='int':  validateCompoundStatements(statement[1],_scope)                
            else:                                     error(statement,"Wrong comparison types")
        elif statement.type == "if": #Recursivo
            if getType(statement[0],_scope) =='int': #We can only compare between ints
                #IF, ELSE
                for block in statement[1:]: 
                    validateCompoundStatements(block,_scope)               
            else:                                                
                error(statement,"Wrong comparison types")
        else: 
            error(statement,f"unkown type {statement.type}")

#This is the right child of an EQUAL Node
def getType(parseNode,scopeNode):
    if parseNode.type == 'ID':
        c = scopeNode.getSymbol(parseNode.value)
        if c: return c[0]
        else: error(parseNode,f"undefined variable {parseNode.value}")
    elif parseNode.type == "ARRAY_POS": 
        c = scopeNode.getSymbol(parseNode.children[0].value)
        #TODO parseNode.children[2] can be an expression with equals, check types??
        if c: return c[0]
        else: error(parseNode,f"undefined variable {parseNode.children[0].value}")
    elif parseNode.type == "INTEGER":  
        return 'int' 
    else: #Opps
        if parseNode.type == 'addop':
            lt = getType(parseNode.children[0],scopeNode)
            rt = getType(parseNode.children[1],scopeNode)
            if lt == rt: return lt
            error(parseNode,f"Wrong types on operator {parseNode.value}")
        if parseNode.type == 'mulop':
            lt = getType(parseNode.children[0],scopeNode)
            rt = getType(parseNode.children[1],scopeNode)
            if lt == rt: return lt
            error(parseNode,f"Wrong types on operator {parseNode.value}")
        if parseNode.type == 'relop':
            lt = getType(parseNode.children[0],scopeNode)
            rt = getType(parseNode.children[1],scopeNode)
            if lt == rt: return lt
            error(parseNode,f"Wrong types on operator {parseNode.value}")
        elif parseNode.type == 'CALL':
            c = getType(parseNode.children[0],scopeNode)
            if len(parseNode.children)>1: 
                f = scopeNode.getSymbol(parseNode.children[0].value)
                for i,passedParam in enumerate(parseNode.children[1:], start=2):
                    if getType(f[i],scopeNode) != getType(passedParam,scopeNode): 
                        error(parseNode,f"Wrong param type: function {parseNode.children[0].value} param #{start-1}")
            return c
        elif parseNode.type == 'param':
            if parseNode.value   == 'ARRAY': return parseNode.children[0].type
            elif parseNode.value == 'VAR':   return parseNode.children[0].type
            else:           error(node,"unexpected param type",parseNode)
        else:
            error(parseNode,"unkown type")

#Recibe como argumento el resultado de la funcion parser() en el archivo parser.py
#Regresa la tabla de simbolos
def tabla(node, imprime = True):    
    st = ScopeTree(tag="program")
    if node.type == "program": #program can only have declarations
        #part of the language
        st.scope["input"] = ('int',defTypes.FUN,None)
        st.scope["output"] = ('void',defTypes.FUN,None)
        for ch in node.children:  
            st.addSymbol(ch)
            if ch.value == "FUNCTION": ScopeTree.appendChildren(st,ch) #RECURSION
    else: error(node,"error, program starts with", ch.type)
    if imprime: st.printAllScopes()
    return st
    
#Recibe como argumento el resultado de la funcion parser() en el archivo parser.py
#Regresa la tabla de simbolos
def semantica(tree, imprime = True):
    
    ts = tabla(tree,imprime)
    
    '''
    TODO
    Utiliza reglas lógicas de inferencia para implementar la semántica de C‐. Ver
    descripción de la semántica de C‐ en el documento en Bb).
    '''
    return None

#Ruben Cuadra A01019102
if __name__ == '__main__':
    # Segundo Parcial
    from globalTypes import *
    from parser import parser, globales
    f = open('examples/3.c-', 'r')
    programa = f.read()
    progLong = len(programa)
    programa = programa + TokenType.ENDFILE.value
    posicion = 0
    
    globales(programa, posicion, progLong)
    AST = parser(False)
    semantica(AST,True)