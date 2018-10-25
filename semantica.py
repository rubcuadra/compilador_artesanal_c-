
class ScopeTree():
    def __init__(self,scope={},parent=None, tag=''):
        self.scope    = dict(scope) #Copy of Dict
        self.parent   = parent
        self.tag      = tag
        self.children = []
    
    def addSymbol(self, s): #Check if it exists before inserting?
        if s.value == "ARRAY":
            self.scope[s.children[1].value] = (f"{s.children[0].type}_arr",s.children[3].value) 
            # for i in range( ch.children[3].value ): st.addSymbol(f'{ch.children[1].value}_{i}',ch.children[0].type) 
        elif s.value == "VAR":
            self.scope[s.children[1].value] = (s.children[0].type,None) #Vars are initialized in None
        elif s.value == "FUNCTION":
            self.scope[s.children[1].value] = (f"{s.children[0].type}_fun",None) #functions are initialized in None
        else: 
            raise Exception("Wrong symbol")

    def inScope(self,var):
        if var in self.scope: return True
        elif self.parent:     return self.parent.inScope(var)
        return False
    
    @staticmethod
    def appendChildren(root, parserNode):
        #Scope is created in this cases
        if parserNode.type == "declaration" and parserNode.value == "FUNCTION": 
            c = ScopeTree(parent=root,tag=parserNode.children[1].value)
            #Set params
            for param in parserNode.children[2:-1]:
                if param.type == 'void': continue #Skip void in params
                c.addSymbol(param)
            #Body
            for statement in parserNode.children[-1].children: #compound_statements
                if statement.type == 'declaration': #Define in the scope
                    c.addSymbol(statement)
                elif statement.type == "EQUALS":    #Validate children exist and children[0].type == children[1].type 
                    pass
                elif statement.type == "CALL":      #Check called func exists
                    pass
                elif statement.type == "return_stmt":  #Check returns exist
                    pass
                elif statement.type in ["while","if","else"]: #Recursivo
                    pass
                else: 
                    print(statement.type)

            root.children.append(c)

    def __str__(self):
        s = ""
        if self.parent: s += str(self.parent)
        s += f"{self.tag}\n"
        for key,val in self.scope.items():
            s += f"\t{val[0]} {key} {val[1]}\n"
        return s

#Recibe como argumento el resultado de la funcion parser() en el archivo parser.py
#Regresa la tabla de simbolos
def tabla(node, imprime = True):    
    st = ScopeTree(tag="program")
    if node.type == "program": #program can only have declarations
        for ch in node.children:  
            st.addSymbol(ch)
            #RECURSION
            if ch.value == "FUNCTION": ScopeTree.appendChildren(st,ch) 
    else:
        raise Exception("error, program starts with", ch.type)

    print(st.children[0])
    

#Recibe como argumento el resultado de la funcion parser() en el archivo parser.py
#Regresa la tabla de simbolos
def semantica(tree, imprime = True):
    ts = tabla(tree,imptime)
    '''
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