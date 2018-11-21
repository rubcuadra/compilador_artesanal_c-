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
    
    def comment(self,text):
        self.f.write("#")
        self.f.write(text.replace("\n","\n#"))
        self.f.write("\n")

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
            defScope = tables.getChildrenScope(defName)
            
            #Define params in that function
            if params[0].type != 'void':
                for p in params:
                    defScope.define(p[1].value,WORD_SIZE) #Define for function 

            generator.writeLine(f"{defName}:", tab=False)
            for statementNode in codeBlock:
                generateCode(statementNode, defScope, generator) 
            
            #Return pointer based on number of declarations
            if retType == 'void' and defName != 'main': #Return at the end of a void, otherwise there must be a return
                if params[0].type != 'void': #Reset after params
                    lastParam = params[-1][1].value
                    offset = defScope.getOffset(lastParam)
                    newSP = offset-WORD_SIZE
                else:
                    newSP = 0
                defScope.setSP( newSP ) #Last param offset + WordSize
                generator.writeLine(f'addi $sp,$sp,{defScope.sp}') #Return flag before declarations in function
                generator.writeLine(f'jr $ra')                     # Jump to addr stored in $ra

        elif node.value == 'VAR':
            varType = node[0].type
            varName = node[1].value
            
            tables.define(varName,WORD_SIZE) #Save offset for that var
            generator.writeLine('li $s0 0')                    #Copy init to s0   
            generator.writeLine('sw $s0,0($sp)')               #Save s0
            generator.writeLine(f'addi $sp,$sp,-{WORD_SIZE}')  #Move Flag

        elif node.value == 'ARRAY':
            arrType = node[0].type
            arrName = node[1].value
            arrSize = node[3].value
            
            tables.define(arrName,WORD_SIZE*arrSize) #Save offset for that array
            for i in range(arrSize):
                generator.writeLine('li $s0 0')                    #Copy init to s0   
                generator.writeLine('sw $s0,0($sp)')               #Save s0
                generator.writeLine(f'addi $sp,$sp,-{WORD_SIZE}')  #Move Flag            
        else:    
            raise Exception(f"unkown declaration {node.type} {node.value}")
    elif node.type == 'if':
        condition = node[0] 
        #LEFT
        generateCode(condition[0], tables, generator)
        generator.writeLine("sw $a0 0($sp)")#Save record
        generator.writeLine(f'addi $sp,$sp,-{WORD_SIZE}') #Move to next record
        tables.setSP( tables.sp + WORD_SIZE )
        #RIGHT
        generateCode(condition[1], tables, generator) #Right in a0
        generator.writeLine("lw $t1 4($sp)")          #Left  in t1
        tables.setSP( tables.sp - WORD_SIZE ) 
        generator.writeLine(f"addi $sp,$sp,{WORD_SIZE}") #Return pointer
        
        trueLabel,falseLabel,contLabel = tables.getIfLabels()
        #t1 RELOP a0
        if condition.value == 'LT':
            generator.writeLine(f"blt $a0, $t1, {trueLabel}") 
        elif condition.value == 'LE':
            generator.writeLine(f"ble $a0, $t1, {trueLabel}") 
        elif condition.value == 'GT':
            generator.writeLine(f"bgt $a0, $t1, {trueLabel}") 
        elif condition.value == 'GE':
            generator.writeLine(f"bge $a0, $t1, {trueLabel}") 
        elif condition.value == 'EQ':
            generator.writeLine(f"beq $a0, $t1, {trueLabel}") 
        elif condition.value == 'NE':
            generator.writeLine(f"bne $a0, $t1, {trueLabel}") 
        else:
            raise Exception("Unkown operator ",condition.value)
        generator.writeLine(f"j {falseLabel}") #If we got here is that we didnt jump before
        generator.writeLine(f"{trueLabel}:", tab=False) 
        for statement in node[1]: 
            generateCode(statement,tables,generator)
        generator.writeLine(f"j {contLabel}") 
        generator.writeLine(f"{falseLabel}:", tab=False) 
        if len(node.children) == 3: #else part
            for statement in node[2]: 
                generateCode(statement,tables,generator)

        generator.writeLine(f"{contLabel}:", tab=False) 
        
        
    elif node.type == 'while':
        condition = node[0]
        codeBlock = node[1]
        '''
            TODO: WHILE structure
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
            defScope = tables.getGlobalScope().getChildrenScope(defName)
            s = tables.getSymbol(defName) #Knowing params of the function
            #Prepare params that will be sent
            current_offset = 0
            for passedVar,paramInDef in zip(callParams,s[2:]) : #Define params for the call 
                #Load to a0 the value that will be sent
                generateCode(passedVar, tables, generator)
                #Save that for passing as params
                generator.writeLine(f'addi $sp,$sp,-{current_offset}')#Move Flag to nextFree
                generator.writeLine('sw $a0,0($sp)')                  #Save that Param
                generator.writeLine(f'addi $sp,$sp, {current_offset}')   #Return Flag
                current_offset += WORD_SIZE
            generator.writeLine(f'addi $sp,$sp,-{current_offset}') #Move Flag to nextFree
            #Call the function
            generator.writeLine(f'jal {defName}')  # Save current PC in $ra, and jump to function
            #IF def returned something it will be in a0
            generator.writeLine(f'addi $sp,$sp,{current_offset}') #Return to the position before setting params
    elif node.type == "return_stmt":
        expr = node[1] #Check if it is a SEMI or something else (SEMI->void)
        generateCode(expr,tables,generator) #Put the return value in a0
        s  = tables.getSymbol(tables.tag)
        lastParam = s[-1][1].value
        offset = tables.getOffset(lastParam)
        newsp = offset-WORD_SIZE
        tables.setSP( newsp ) #Last param offset + WordSize
        generator.writeLine(f'addi $sp,$sp,{tables.sp}') #Return flag before declarations in function
        generator.writeLine(f'jr $ra') # Jump to addr stored in $ra
    elif node.type == 'EQUALS':
        left     = node[0]
        right    = node[1]
        generateCode(right,tables,generator) #Puts right result to a0
        if left.type == "ARRAY_POS":
            arrName = left[0].value
            ix      = left[2].value
            if tables.isGlobal(arrName):
                generator.writeLine(f"la $a1, {arrName}{ix}") #Get address 
                generator.writeLine(f"sw $a0 0($a1)")      
            else:
                spOffset = tables.getOffset(arrName)
                generator.writeLine(f"sw $a0, {spOffset-ix*WORD_SIZE}($sp)")
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
        generateCode(l,tables,generator)    #Puts result in a0
        generator.writeLine("sw $a0 0($sp)")#Save record
        generator.writeLine(f'addi $sp,$sp,-{WORD_SIZE}') #Move to next record
        tables.setSP( tables.sp + WORD_SIZE )
        generateCode(r,tables,generator)    #Puts result in a0
        generator.writeLine("lw $t1 4($sp)")#Load saved record to t1
        #Put result t1*a0 in a0 || Put result t1/a0 in a0 
        if node.value=='TIMES': 
            generator.writeLine("mult $t1, $a0") #Result goes to HI and LO
            generator.writeLine("mflo $a0")      #we will only use LO (32 bits)
        else:                   
            generator.writeLine("div $t1, $a0")  #Result goes to HI and LO
            generator.writeLine("mflo $a0")      #we will only use Quotient (LO)
        tables.setSP( tables.sp - WORD_SIZE )
        generator.writeLine(f"addi $sp,$sp,{WORD_SIZE}") #Return pointer
    elif node.type == 'addop':
        l = node[0]
        r = node[1]
        op = node.value #PLUS MINUS
        generateCode(l,tables,generator)    #Puts result in a0
        generator.writeLine("sw $a0 0($sp)")#Save record
        generator.writeLine(f'addi $sp,$sp,-{WORD_SIZE}') #Move to next record
        tables.setSP( tables.sp + WORD_SIZE )
        generateCode(r,tables,generator)    #Puts result in a0
        generator.writeLine("lw $t1 4($sp)")#Load saved record to t1
        #Put result t1-a0 in a0 || Put result t1+a0 in a0 
        if node.value=='PLUS': generator.writeLine("add $a0 $t1 $a0") 
        else:                  generator.writeLine("sub $a0 $t1 $a0")
        tables.setSP( tables.sp - WORD_SIZE ) 
        generator.writeLine(f"addi $sp,$sp,{WORD_SIZE}") #Return pointer
    elif node.type == "INTEGER":
        generator.writeLine(f"li $a0, {node.value}")   #Load to a0
    elif node.type == "ARRAY_POS": #Access to array by index
        arrName = node[0].value
        ix      = node[2].value
        if tables.isGlobal(arrName):
            generator.writeLine(f"lw $a0, {arrName}{ix}")
        else:
            spOffset = tables.getOffset(arrName)
            generator.writeLine(f"lw $a0, {spOffset-ix*WORD_SIZE}($sp)")            
    elif node.type == "ID":
        varName = node.value
        if tables.isGlobal(varName): 
            generator.writeLine(f"lw $a0, {varName}")
        else:
            s = tables.getSymbol(varName)
            spOffset = tables.getOffset(varName)
            generator.writeLine(f"lw $a0, {spOffset}($sp)")
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