from enum import Enum

def error(node,msg):
    if node.token:raise Exception(f"ERROR LINE {node.token.lineno+1}, CHAR {node.token.lexpos+1} - {msg}")    
    else:         
        print(node)
        raise Exception(f"ERROR : {msg}")


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
        self.sp       = 0
        if parent == None: self.depth = 0
        else:              self.depth = None
    
    def getChildrenScope(self,tag): #Search between children
        if self.tag == tag: return self
        for ch in self.children:
            if ch.getChildrenScope(tag)!=None: 
                return ch

    #Reset pointer to params start (sp = lastParamoffset)
    def setSP(self, newSP):
        self.sp = newSP

    def getGlobalScope(self):
        if self.parent: return self.parent.getGlobalScope()
        return self
    
    def define(self, symbol, wordSize):
        if symbol in self.scope:
            if self.parent == None: #GLOBAL, use $gp
                raise Exception("Modified globals logic")
                # self.scope[symbol][-1] = self.gp 
                # self.gp += wordSize
                # print(symbol,' gp ',self.scope[symbol][-1])
            else:                   #CURRENT, Use $sp
                self.scope[symbol][-1] = self.sp 
                self.sp += wordSize
                # print(symbol,' sp ',self.scope[symbol][-1])
        else: #Go Up
            raise Exception("Not in this scope") #Redefinition of a var??

    def isGlobal(self,symbol):
        if symbol in self.scope and self.parent == None: return True
        elif self.parent != None: return self.parent.isGlobal(symbol)
        return False

    def getOffset(self,symbol):
        if symbol in self.scope:
            if self.parent == None: 
                raise Exception("Shouldn't be here, globals have different logic")
            else: #CURRENT, Use $sp
                offset = self.scope[symbol][-1] 
                return self.sp-offset
        elif self.parent != None: #It is a global variable(or maybe just upper scope)
            return self.parent.getOffset(symbol)
        else:                 
            raise Exception(f"Undefined symbol {symbol}")
        

    #dataType, strucType, value
    def addSymbol(self, s):  #Last pos in Arr,Var is for $sp and $gp flags
        #Check if it already exists before inserting?
        if s.value == "ARRAY":
            self.scope[s.children[1].value] = [s.children[0].type,defTypes.ARR,s.children[3].value,None]
            # for i in range( ch.children[3].value ): st.addSymbol(f'{ch.children[1].value}_{i}',ch.children[0].type) 
        elif s.value == "VAR":
            self.scope[s.children[1].value] = [s.children[0].type,defTypes.VAR,None] #Vars are initialized in None
        elif s.value == "FUNCTION":
            self.scope[s.children[1].value] = [s.children[0].type,defTypes.FUN,*s.children[2:-1]] #functions are initialized in None
        else: 
            error(s,"Wrong declaration")

    def getSymbol(self,var): 
        # for k in self.scope: print(k)
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
        return self.printFromBottom(level=self.getDepth())

    def getDepth(self):
        if   self.depth:  return self.depth
        elif self.parent: self.depth = 1+self.parent.getDepth()
        return            self.depth

    def printFromBottom(self,level=0):
        s = ""
        if self.parent: s += self.parent.getStr(level-1)
        s += '\t'*level
        s += f"{self.tag}\n"
        for key,val in self.scope.items():
            s += '\t'*(level+1)
            s += f"{val[0]} {key} - {val[1].value} {val[2:]}\n"
        return s + "\n"

    def getStr(self, level=0):
        s = ""
        s += '\t'*level
        s += f"{self.tag}\n"
        for key,val in self.scope.items():
            s += '\t'*(level+1)
            s += f"{val[0]} {key} - {val[1].value} {val[2:]}\n"
        return s

    #Goes to a leaf and prints the scope
    def printAllScopes(self):
        print(self.getStr(level=self.getDepth()))
        if self.children:
            for ch in self.children:
                ch.printAllScopes()

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
            params = statement[1:]
            s = getType(statement[0],_scope)
            if not s:     
                error(statement,f"Calling function without definition '{statement[0].value}'")
            if s!='void': 
                error(statement,f"Called NON void function without assignment")
            symb = _scope.getSymbol(statement[0].value)
            if statement[0].value == 'output': #Param is an int 
                if len(params)!=1: raise Exception("output only recieves 1 int param")
                else:
                    s = getType(params[0],_scope)
                    if s != "int": raise Exception("calling input with a non int value")
            else:
                if len(symb[2:]) != len(params): raise Exception(f"Calling function with different amount of params: {statement[0].value}")
                for passed,param in zip(symb[2:],params):
                    if passed[0].type == 'int' and param.type == 'INTEGER':
                        continue
                    raise Exception("Calling function with different type of params")

        elif statement.type == "return_stmt":  #Check returns exist
            s = _scope.getSymbol(_scope.tag) #SI es None es que we fucked up algo
            if s[0] == 'void' and len(statement.children)>1: 
                if statement[1].type == "SEMI": continue
                error(statement,"ERROR: void function returning values")
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
        if parseNode.children[2]==None: error(parseNode,"Wrong access to array") 
        t = getType(parseNode.children[2],scopeNode)
        if t != 'int': error(parseNode,f"wrong access to array, index of type {t}")
        #TODO parseNode.children[2] can be an expression with equals, check types??
        if c: return c[0]
        else: error(parseNode,f"undefined variable {parseNode.children[0].value}")
    elif parseNode.type == "INTEGER":  
        return 'int' 
    elif parseNode.type == "SEMI":
        return 'void'
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
                if len(f[2:])!=len(parseNode.children[1:]): raise Exception(f"Calling function with different amount of params: {parseNode.children[0].value}")
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
    return True

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