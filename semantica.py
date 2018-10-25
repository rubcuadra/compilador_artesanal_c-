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
    
    #dataType, strucType, value
    def addSymbol(self, s): #Check if it exists before inserting?
        if s.value == "ARRAY":
            self.scope[s.children[1].value] = (s.children[0].type,defTypes.ARR,s.children[3].value) 
            # for i in range( ch.children[3].value ): st.addSymbol(f'{ch.children[1].value}_{i}',ch.children[0].type) 
        elif s.value == "VAR":
            self.scope[s.children[1].value] = (s.children[0].type,defTypes.VAR,None) #Vars are initialized in None
        elif s.value == "FUNCTION":
            self.scope[s.children[1].value] = (s.children[0].type,defTypes.FUN,None) #functions are initialized in None
        else: 
            raise Exception("Wrong symbol")

    def getSymbol(self,var): 
        if var in self.scope: return self.scope[var]
        elif self.parent:     return self.parent.getSymbol(var)
        else:                 return None

    @staticmethod
    def appendChildren(root, parserNode, scope=None):
        #Scope is created in this cases
        if parserNode.type == "declaration" and parserNode.value == "FUNCTION": 
            _scope = ScopeTree(parent=root,tag=parserNode.children[1].value)
            #Set params
            for param in parserNode.children[2:-1]:
                if param.type == 'void': continue #Skip void in params
                _scope.addSymbol(param)
            #Body -> compound_statements
            for statement in parserNode.children[-1].children: 
                if statement.type == 'declaration': #Define it in the scope
                    _scope.addSymbol(statement)
                elif statement.type == "EQUALS":    #Validate var exist and check that assign is of the same type
                    s = _scope.getSymbol(statement.children[0].value)
                    if s:
                        gt = getType(statement.children[1],_scope)
                        if s[0] == gt: continue
                        raise Exception(f"Wrong data type assignment: {s[0]} {statement.children[0].value} => {gt}")
                    else: 
                        raise Exception(f"Var does not exist {statement.children[0].value}")
                elif statement.type == "CALL":      #Check called func exists and it is void
                    s = _scope.getSymbol(statement.children[0].value)
                    if not s:        raise Exception(f"Calling function without definition '{statement.children[0].value}'")
                    if s[0]!='void': raise Exception(f"Called NON void function without assignment")
                elif statement.type == "return_stmt":  #Check returns exist
                    pass #TODO
                elif statement.type in ["while","if","else"]: #Recursivo
                    pass #TODO
                else: 
                    raise Exception(f"unkown type {statement.type}")
            root.children.append(_scope)
        elif False: #Case while,if,else. Scope must be something
            pass #TODO

    def __str__(self):
        s = ""
        if self.parent: s += str(self.parent)
        s += f"{self.tag}\n"
        for key,val in self.scope.items():
            s += f"\t{val[0]} {key} - {val[1].value}\n"
        return s

#This is the right child of an EQUAL Node
def getType(parseNode,scopeNode):
    if parseNode.type == 'ID':
        c = scopeNode.getSymbol(parseNode.value)
        return c[0]
    elif parseNode.type == "ARRAY_POS": 
        c = scopeNode.getSymbol(parseNode.children[0].value)
        #TODO parseNode.children[2] can be an expression with equals, check types??
        return c[0]
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
        elif parseNode.type == 'CALL':
            c = getType(parseNode.children[0],scopeNode)
            if len(parseNode.children)>1: print("TODO",c) #TODO validate params exist
            return c
        else:
            print('TODO',parseNode.type, parseNode.value)
    return 'int'

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
    else:
        raise Exception("error, program starts with", ch.type)

    for c in st.children: print(c)
    

#Recibe como argumento el resultado de la funcion parser() en el archivo parser.py
#Regresa la tabla de simbolos
def semantica(tree, imprime = True):
    ts = tabla(tree,imptime)
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
    
    t = tabla(AST)