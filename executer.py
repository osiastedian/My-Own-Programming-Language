from interpreter import Interpreter
from enum import Enum
import re
class Executer:

    class Statment:
        def __init__(self, code:int = -1, line: str = ""):
            self.code = code  
            self.line = line

    class Variable:
        def __init__(self, name: str, value: str, vType: str):
            self.name = name
            self.type = vType
            self.setValue(value)
        
        def __str__(self):
            return self.name + ","+ str(self.value)+","+self.type
        
        def setValue(self, val:str):
            if(self.type == "CHAR"):
                self.value = val.replace('\'','')
            elif(self.type == "FLOAT"):
                self.value = float(val)
            elif(self.type == "INT"):
                self.value = int(val)
            else:
                self.value = val
            # print(self.type,":[", self.value,"]")
        def getValue(self):
            return self.value
        
        def getName(self):
            return self.name

    class Code(Enum):
        ERROR = -1
        INIT_STATEMENT = 0
        COMMENT_STATEMENT = 1
        START_STATEMENT = 2
        STOP_STATEMENT = 3
        OUTPUT_STATEMENT = 4
        ASSIGNMENT_STATEMENT = 5
        

    def __init__(self):
        self.interpreter = Interpreter()
        self.parsed = []
        self.memory = {}
        self.programStarted: bool = False
        self.programStopped: bool = True
    
    def executeProgram(self, strLines):
        for line in strLines:
            stmt = self.Statment(self.getCode(line), line)
            self.parsed.append(stmt)
        for stmt in self.parsed:
            if(stmt.code == self.Code.COMMENT_STATEMENT):
                continue
            elif(stmt.code == self.Code.INIT_STATEMENT):
                self.execute_INIT_STATEMENT(stmt.line)
            elif(stmt.code == self.Code.START_STATEMENT):
                self.execute_START_STATEMENT()
            elif(stmt.code == self.Code.STOP_STATEMENT):
                self.execute_STOP_STATEMENT()
            elif(stmt.code == self.Code.ASSIGNMENT_STATEMENT):
                self.execute_ASSIGNMENT_STATEMENT(stmt.line)
            elif(stmt.code == self.Code.OUTPUT_STATEMENT):
                self.execute_OUTPUT_STATEMENT(stmt.line)
            else:
                self.execute_OUTPUT_STATEMENT(stmt.line)
            print('Code:', stmt.code,'\t\t=',stmt.line)
    
    def execute_INIT_STATEMENT(self, strLine):
        terms = self.removeGarbageFromArray(re.split("(VAR)|(AS)|(INT)|(CHAR)|(BOOL)|(FLOAT)|(,)", strLine))
        # Get Type
        varType = terms[-1]
        # Get Initializations
        for term in terms:
            term = term.strip()
            defaultValue = self.getDefaultValueOfType(varType)
            if(self.interpreter.isKeyWord(term)):
                continue
            elif(self.interpreter.isValidIdentifier(term)):
                self.addVariable(term, defaultValue, varType)
            elif(self.interpreter.isValidAssignmentStatement(term)):
                newTerm = term.split('=')
                self.addVariable(newTerm[0],newTerm[1],varType)
    
    def execute_START_STATEMENT(self):
        self.programStarted = True
        self.programStopped = False

    def execute_STOP_STATEMENT(self):
        self.programStarted = False
        self.programStopped = True

    def execute_ASSIGNMENT_STATEMENT(self, strLine):
        # print("HI:",strLine)
        terms = self.removeGarbageFromArray(re.split(' |(\=\=)|(\=)', strLine))
        equation = ""
        indexOfEQ = 0
        for i, e in reversed(list(enumerate(terms))):
            if e == "=":
                break
            equation = e + equation
            indexOfEQ = i
        del terms[indexOfEQ:]
        isBooleanEquation = self.interpreter.isValidBooleanOperation(equation)
        if(isBooleanEquation):
            eqTerms = re.split(' |(\()|(\))|(\=\=)|(\<\=)|(\>\=)|(\&\&)|(\|\|)|(\<)|(\>)',equation)
        else:
            eqTerms = re.split(' |(\+)|(\/)|(\-)|(\*)|(\()|(\))',equation)
        eqTerms = self.removeGarbageFromArray(eqTerms)
        
        nodeList = []
        for term in eqTerms:
            temp = Interpreter.Node(term)
            nodeList.append(temp)
        if isBooleanEquation:
            node = self.nodeCreate(nodeList, ["==","<=",">=","<",">","&&","||"])
        else:
            node = self.nodeCreate(nodeList)
        val = self.evaluateNode(node)
        print("Value", val)
        variables = [x for x in terms if x is not '=']
        for variable in variables:
            self.setVariable(variable, val)

    def evaluateNode(self, node):
        return self.postOrder(node)
    
    def postOrder(self, node):
        if node == None:
            return None
        elif node.left == None and node.right == None:
            if self.interpreter.isValidNumericConstant(node.value):
                return float(node.value) if "." in node.value else int(node.value)
            elif self.interpreter.isValidBooleanConstant(node.value):
                return True if node.value == "TRUE" else False
            elif self.interpreter.isValidIdentifier(node.value):
                return self.getVariableData(node.value)
            else:
                return node.value
        else:
            left = self.postOrder(node.left)
            right = self.postOrder(node.right)
            result = 0
            operation = node.value
            # print("Left:", left, "Right:", right, "Operation", operation)
            if operation == "*":
                result = left * right
            elif operation == "/":
                result = left / right
            elif operation == "+":
                result = left + right
            elif operation == "-":
                result = left - right
            #boolean operations
            elif operation == "==":
                result = left == right
            elif operation == "<=":
                result = left <= right
            elif operation == ">=":
                result = left >= right
            elif operation == "<":
                result = left < right
            elif operation == ">":
                result = left > right
            elif operation == "&&":
                result = left and right
            elif operation == "||":
                result = left or right
            else:
                result = None
            print("Result:", result)
            return result

    def execute_OUTPUT_STATEMENT(self, strLine):
        terms = self.removeGarbageFromArray(re.split('OUTPUT:|&',strLine))
        outputStr = ""
        outputLines = []
        for term in terms:
            if(self.interpreter.isValidIdentifier(term)):
                outputStr+= str(self.getVariableData(term))
            elif(self.interpreter.isNewLine(term)):
                outputLines.append(outputStr)
                outputStr = ""
            elif(self.interpreter.isValidStringConstant(term)):
                term = term.replace('"','')
                outputStr+= term
        outputLines.append(outputStr)
        print(outputLines)
        return outputLines

    def removeGarbageFromArray(str, terms, strip = True):
        terms = [x for x in terms if x is not None]
        terms = [x for x in terms if x is not ' ']
        terms = [x for x in terms if x is not '']
        if(strip):
            terms = [x.strip() for x in terms]
        return terms

    def getDefaultValueOfType(self, varType: str):
        switch = {
            "INT": 0,
            "BOOL": False,
            "CHAR": '',
            "FLOAT": 0.0
        }
        return switch.get(varType, None)
    
    def addVariable(self, name: str, initVal: str, varType: str):
        if(not(self.programStarted)):
            self.memory[name] = self.Variable(name,initVal,varType)
        else:
            raise

    def setVariable(self, name:str, newVal: str):
        if(name in self.memory):
            self.memory[name].setValue(newVal)
        else:
            print(name,"caused an exception")
            raise
    
    def getVariableData(self, name:str):
        if(name in self.memory):
            return self.memory[name].getValue()
        else:
            raise

    def getCode(self, strLine):
        if(self.interpreter.isValidInitializationStatement(strLine)):
            return self.Code.INIT_STATEMENT
        if(self.interpreter.isValidCommentStatement(strLine)):
            return self.Code.COMMENT_STATEMENT
        if(self.interpreter.isValidStartStatement(strLine)):
            return self.Code.START_STATEMENT
        if(self.interpreter.isValidStopStatement(strLine)):
            return self.Code.STOP_STATEMENT
        if(self.interpreter.isValidOutputStatement(strLine)):
            return self.Code.OUTPUT_STATEMENT
        if(self.interpreter.isValidAssignmentStatement(strLine)):
            return self.Code.ASSIGNMENT_STATEMENT
        return self.Code.ERROR
    
    def findPair(self,nodeList: [], index):
        stack = []
        retIndex = index
        for node in nodeList:
            if(node.value == '('):
                stack.append(node.value)
            elif(node.value == ')'):
                stack.pop()
            if len(stack) == 0:
                break
            retIndex = retIndex + 1
        return retIndex

    def nodeCreate(self,nodeList:[], operationSequence = ['*','/','+','-']):
        index = 0
        # print("Node List Start:", nodeList)
        while index < len(nodeList):
            if (nodeList[index].value == '('):
                pairIndex= self.findPair(nodeList[index:],index)
                removedList = nodeList[index:pairIndex+1]
                del removedList[0]
                del removedList[-1]
                node = self.nodeCreate(removedList, operationSequence)
                del nodeList[index:pairIndex+1]
                node.value = str(self.postOrder(node))
                node.left = node.right = None
                nodeList.insert(index,node)
            index = index + 1
        for operation in operationSequence:
            index = 0
            while index < len(nodeList):
                if(nodeList[index].value == operation):
                    if(index+1 < len(nodeList)):
                        nodeList[index].right = nodeList[index+1]
                        del nodeList[index+1]
                    if(index-1 >= 0):
                        nodeList[index].left = nodeList[index-1]
                        del nodeList[index-1]
                index = index + 1
        # print("Node List End:", nodeList)
        return nodeList[0]



exec = Executer()

strLines = [
'* my first program in CFPL',
'VAR abc, b, c AS FLOAT',
'VAR x, w_23=’w’ AS CHAR',
'VAR samp1, samp2, samp3 AS BOOL',
'VAR t=TRUE AS BOOL',
'START',
'abc = b = 100 + (3.33 * 3 )',
'b = b + abc',
'c = b',
't = abc == b',
"w_23='a'",
'* this is a comment',
'OUTPUT: t',
'OUTPUT: abc & " " &  b & " hi " & c & # & w_23 & "[#]"',
'STOP'
]
exec.executeProgram(strLines)
