from semantica import tabla
WORD_SIZE = 4 #Bytes

class CodeGenerator(object):
    """docstring for CodeGenerator"""
    def __init__(self, filePath):
        super(CodeGenerator, self).__init__()
        self.filePath = filePath
    
    def __enter__(self):
        self.openFile()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.closeFile()

    def openFile(self):
        self.f = open(self.filePath, "w+")

    def closeFile(self):
        self.f.close()

    def writeLine(self, text, breakLine=True, tab=True):
        if tab: self.f.write("\t")
        self.f.write(text)
        if breakLine: self.f.write("\n")

def exit(generator):
    generator.writeLine("li $v0, 10") #Exit call
    generator.writeLine("syscall")

def generateCode(node, tables, generator):
    if node.type == 'declaration':
        if node.value == 'FUNCTION':      #Declare Params
            retType   = node[0].type             
            defName   = node[1].value
            params    = node[2:-1]   
            codeBlock = node[-1]
            '''
                TODO: Function Declaration
            '''
            generator.writeLine(f"{defName}:", tab=False)
            for statementNode in codeBlock:
                generateCode(statementNode, tables.getChildrenScope(defName), generator) 

        elif node.value == 'VAR':
            varType = node[0].type
            varName = node[1].value
            '''
                TODO: CHECAR ARREGLOS
            '''
            tables.define(varName,WORD_SIZE) #Save offset for that var
            generator.writeLine('li $s0 0')                    #Copy init to s0   
            generator.writeLine('sw $s0,0($sp)')               #Save s0
            generator.writeLine(f'addi $sp,$sp,-{WORD_SIZE}')  #Move Flag

        elif node.value == 'ARRAY':
            arrType = node[0].type
            arrName = node[1].value
            arrSize = node[3].value
            '''
                TODO: ARR Declaration
            '''
        else:    
            raise Exception(f"unkown declaration {node.type} {node.value}")
    elif node.type == 'if':
        condition = node[0] #type == relop
        # condition[0] condition.value(EQ, LT, GT ... ) condition[1]
        condTrue  = node[1]
        condFalse = node[2]
        '''
            TODO: IF structure
        '''
    elif node.type == 'EQUALS':
        left     = node[0]
        right    = node[1]
        
        generateCode(right,tables,generator)
        '''
            TODO: CHECAR ARREGLOS
        '''
        if left.type == "ARRAY_POS":
            arrName = left[0].value
            ix      = left[2].value
            if tables.isGlobal(arrName):
                generator.writeLine(f"la $a1, {arrName}{ix}") #Get address 
                generator.writeLine(f"sw $a0 0($a1)")      
            else:
                print("MISSING TO IMPLEMNT ACCESS TO LOCAL ARRAYS")
                print(left)
        elif left.type == 'ID':
            assigned = left.value
            #Save whatever is in $a0 in the variable
            if tables.isGlobal(assigned):
                generator.writeLine(f"la $a1, {assigned}") #get address of global var
                generator.writeLine(f"sw $a0 0($a1)")      #save $a0 value in $a1
            else:
                spOffset = tables.getOffset(assigned)
                generator.writeLine(f"sw $a0, {spOffset}($sp)")
        else:
            raise Exception("Unkown type on left side of equals")
        
    elif node.type == 'mulop':
        l  = node[0]
        r  = node[1]
        op = node.value #TIMES DIVIDE
        '''
            TODO: MULTI / DIV
        '''
    elif node.type == 'addop':
        l = node[0]
        r = node[1]
        op = node.value #PLUS MINUS
        '''
            TODO: SUMA / RESTA
        '''
    elif node.type == 'CALL':
        defName    = node[0].value
        callParams = node[1:] #Can Be []
        if defName == 'input': 
            generator.writeLine("li $v0, 5")     #Will read
            generator.writeLine("syscall")       #Reads and saves the int in $v0
            generator.writeLine("move $a0, $v0") #Move it to a0
        elif defName == 'output':
            generateCode( callParams[0], tables, generator ) #Puts Result in $a0
            generator.writeLine("li $v0, 1")     #Will Print
            generator.writeLine("syscall")       #Print the value of $a0
        else:
            '''
                TODO: CALL the already defined Function
                Escribir los parametros, guardar el numero de params en una var
            '''
    elif node.type == "INTEGER":
        generator.writeLine(f"li $a0, {node.value}")   #Load to a0
    elif node.type == "ARRAY_POS": #Access to array by index
        arrName = node[0].value
        ix      = node[2].value
        if tables.isGlobal(arrName):
            generator.writeLine(f"lw $a0, {arrName}{ix}")
        else:
            print("MISSING TO IMPLEMNT READ TO LOCAL ARRAYS")
    elif node.type == "ID":
        varName = node.value
        if tables.isGlobal(varName): 
            generator.writeLine(f"lw $a0, {varName}")
        else:
            spOffset = tables.getOffset(varName)
            generator.writeLine(f"lw $a0, {spOffset}($sp)")
    elif node.type == "return_stmt":
        expr = node[1] #Check if it is a SEMI or something else (SEMI->void)
        '''
            TODO: Return value is stored in $v0, finish with: jr $ra
        '''
    elif node.type == "program": #Start of the code
        #Trick for main structure
        generator.writeLine(f".text")
        generator.writeLine(f".globl main")
        
        #Declare Functions
        for declaration in node: 
            if declaration.value == 'FUNCTION':
                generateCode(declaration,tables,generator) 
                if declaration[1].value == 'main':
                    exit(generator)

        #Declare global variables/arrays
        generator.writeLine(f"")
        generator.writeLine(f".data")
        for declaration in node: 
            varName = declaration[1].value
            if declaration.value != 'FUNCTION': 
                if declaration.value == 'VAR':
                    generator.writeLine(f"{varName}:\t.word 0", tab=False) #Init in 0
                elif declaration.value == 'ARRAY':
                    arrSize = declaration[3].value
                    for i in range(arrSize):
                        generator.writeLine(f"{varName}{i}:\t.word 0", tab=False) #Init in 0
                else:
                    raise Exception("Unkown global declaration")
    else:    
        raise Exception(f"Missing to define type: {node.type} val: {node.value}")
        
def codeGen(tree, filePath):
    st = tabla(tree, False)    
    with CodeGenerator(filePath) as cg:
        generateCode(tree,st,cg)

if __name__ == '__main__':
    # Parcial Final
    from globalTypes import *
    from parser import *
    
    f = open('examples/0.c-', 'r')
    programa = f.read()
    progLong = len(programa)
    programa = programa + TokenType.ENDFILE.value
    posicion = 0
    
    globales(programa, posicion, progLong)
    AST = parser(False)
    
    codeGen(AST, 'program.asm')