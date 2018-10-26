from enum import Enum

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
            raise Exception("Wrong declaration")

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
            raise Exception("Wrong declaration")

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
        else: raise Exception(f"Wrong return type on function {_scope.tag}")
    elif statementBlock.type != 'compound_statements': raise Exception("Not a statement block ",statementBlock)
    #Body -> compound_statements
    for statement in statementBlock.children: 
        if statement.type == 'declaration': #Define it in the scope
            _scope.addSymbol(statement)
        elif statement.type == "EQUALS":    #Validate var exist and check that assign is of the same type
            if statement[0].type in ["ARRAY_POS", "ID"]:
                s = getType(statement[0],_scope)
                gt = getType(statement[1],_scope)
                if s == gt and s!=None: continue
                raise Exception(f"Wrong data type assignment: {s[0]} {statement[0].value} => {gt}")
            else:
                raise Exception("Wrong assignment")
        elif statement.type == "CALL":      #Check called func exists and it is void
            s = getType(statement[0],_scope)
            if not s:     raise Exception(f"Calling function without definition '{statement[0].value}'")
            if s!='void': raise Exception(f"Called NON void function without assignment")
        elif statement.type == "return_stmt":  #Check returns exist
            s = _scope.getSymbol(_scope.tag) #SI es None es que we fucked up algo
            if s[0] == 'void' and len(statement.children)>1: raise Exception("ERROR: void function returning values")
            t = getType(statement[1],_scope)
            if s[0] == t: continue
            raise Exception(f"Wrong return type {s[0]} != {t}")
        elif statement.type == "while":
            #We can only compare between ints
            if getType(statement[0],_scope) =='int':  validateCompoundStatements(statement[1],_scope)                
            else:                                     raise Exception("Wrong comparison types")
        elif statement.type == "if": #Recursivo
            if getType(statement[0],_scope) =='int': #We can only compare between ints
                #IF, ELSE
                for block in statement[1:]: 
                    validateCompoundStatements(block,_scope)               
            else:                                                
                raise Exception("Wrong comparison types")
        else: 
            raise Exception(f"unkown type {statement.type}")

#This is the right child of an EQUAL Node
def getType(parseNode,scopeNode):
    if parseNode.type == 'ID':
        c = scopeNode.getSymbol(parseNode.value)
        if c: return c[0]
        else: raise Exception(f"undefined variable {parseNode.value}")
    elif parseNode.type == "ARRAY_POS": 
        c = scopeNode.getSymbol(parseNode.children[0].value)
        #TODO parseNode.children[2] can be an expression with equals, check types??
        if c: return c[0]
        else: raise Exception(f"undefined variable {parseNode.children[0].value}")
    elif parseNode.type == "INTEGER":  
        return 'int' 
    else: #Opps
        if parseNode.type == 'addop':
            lt = getType(parseNode.children[0],scopeNode)
            rt = getType(parseNode.children[1],scopeNode)
            if lt == rt: return lt
            raise Exception("Wrong types on addop")
        if parseNode.type == 'mulop':
            lt = getType(parseNode.children[0],scopeNode)
            rt = getType(parseNode.children[1],scopeNode)
            if lt == rt: return lt
            raise Exception("Wrong types on mulop")
        if parseNode.type == 'relop':
            lt = getType(parseNode.children[0],scopeNode)
            rt = getType(parseNode.children[1],scopeNode)
            if lt == rt: return lt
            raise Exception("Wrong types on relop")
        elif parseNode.type == 'CALL':
            c = getType(parseNode.children[0],scopeNode)
            if len(parseNode.children)>1: 
                f = scopeNode.getSymbol(parseNode.children[0].value)
                for i,passedParam in enumerate(parseNode.children[1:], start=2):
                    if getType(f[i],scopeNode) != getType(passedParam,scopeNode): 
                        raise Exception(f"Wrong param type: function {parseNode.children[0].value} param #{start-1}")
            return c
        elif parseNode.type == 'param':
            if parseNode.value   == 'ARRAY': return parseNode.children[0].type
            elif parseNode.value == 'VAR':   return parseNode.children[0].type
            else:           raise Exception("unexpected param type",parseNode)
        else:
            raise Exception("unkown type", parseNode)

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
    else: raise Exception("error, program starts with", ch.type)
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
    f = open('examples/2.c-', 'r')
    programa = f.read()
    progLong = len(programa)
    programa = programa + TokenType.ENDFILE.value
    posicion = 0
    
    globales(programa, posicion, progLong)
    AST = parser(False)
    semantica(AST,True)