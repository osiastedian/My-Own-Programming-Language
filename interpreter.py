from parser import CharacterParser
import re

from enum import Enum

class Interpreter:

    class Node:
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None
        def __repr__(self):
            return str(self.__dict__)

    class Code(Enum):
        ERROR = -1
        VAR = 0
        IDENTIFIER = 1
        COMMA = 2
        AS = 3
        DATA_TYPE = 4
        START = 5
        STOP = 6
        COMMENT_OP = 7
        NEWLINE = 8
        CONCATENATOR = 9
        OUTPUT = 10
        STRING_CONST = 11
        ARITHMETIC_OP = 12
        NUMERIC_CONST = 13
        BOOLEAN_CONST = 14
        CHARACTER_CONST = 15
        EQUAL = 16
        IF = 17
        INPUT = 18
        ELSE = 19

        ASSIGNMENT_STMT = 100
    
    def __init__(self):
        self.charParser = CharacterParser()
        self.memory = []
    
    # STATEMENTS
    def validate(self, terms, startState, finalStates, deadStates, table, switcher, coder = None, debug = False, anyInputCode = -1, customGetCode = None):
        if(debug):
            print(terms)
        state = startState
        for term in terms:
            if((term is not None) & (term is not '')):
                if(coder is None):
                    code = self.getCode(term)
                else:
                    code = coder.getCode(term)
                if(code == self.Code.ERROR and customGetCode != None):
                    code = customGetCode(term)
                code = switcher.get(code, -1)
                if(code == self.Code.ERROR):
                    code = anyInputCode if anyInputCode != None else code
                if(debug):
                    print('TERM', term, 'state: ', state, 'code: ', code, 'Sub Error:', anyInputCode)
                state = table[code][state]
                if(debug & (state in deadStates)):
                    print(term, 'is DEAD code:', code)
                    break
        return state in finalStates

    def isValidInitializationStatement(self, strLine, debug = False):
        state = 1
        table = [
        #    0  1  2  3  4  5
            [0, 2, 0, 0, 0, 0], # VAR
            [0, 0, 3, 0, 0, 0], # identifier
            [0, 0, 0, 2, 0, 0], # COMMA
            [0, 0, 0, 4, 0, 0], # AS
            [0, 0, 0, 0, 5, 0], # Data Type
            [0, 0, 3, 0, 0, 0]  # AssignmentOperator
        ]
        
        # terms = re.split(' |(\,)', strLine)
        terms = self.removeGarbageFromArray(re.split("(VAR)|(AS)|(INT)|(CHAR)|(BOOL)|(FLOAT)|(,)", strLine))
        finalStates = [ 5 ]
        deadStates = [ 0 ]
        mySwitcher = {
            self.Code.VAR: 0,
            self.Code.IDENTIFIER : 1,
            self.Code.COMMA: 2,
            self.Code.AS: 3,
            self.Code.DATA_TYPE: 4,
            self.Code.ASSIGNMENT_STMT : 5
        }
        # Todo: Create Custome Get Code if ERROR is Caught
        def customCode (str):
            if(self.isValidAssignmentStatement(str)):
                return self.Code.ASSIGNMENT_STMT
            return self.Code.ERROR
        
        return self.validate(terms,state,finalStates, deadStates, table, mySwitcher, None, debug, None, customCode)
        
    def isValidCommentStatement(self, strLine, debug = False):
        state = 1
        table = [
        #    0  1  2
            [0, 2, 2], # *
            [0, 0, 2] # Any
        ]
        terms = re.split(' ',strLine)
        finalStates = [ 2 ]
        deadStates = [ 0 ]
        mySwitcher = {
            self.Code.COMMENT_OP: 0
        }
        return self.validate(terms,state,finalStates, deadStates, table, mySwitcher, None, debug, 1)

    def isValidStartStatement(self, strLine, debug = False):
        state = 1
        table = [
        #    0  1  2
            [0, 2, 0], # START
            [0, 0, 0] # Others
        ]
        terms = re.split(' ',strLine)
        finalStates = [ 2 ]
        deadStates = [ 0 ]
        mySwitcher = {
            self.Code.START: 0
        }
        return self.validate(terms,state,finalStates, deadStates, table, mySwitcher, None, debug, 1)

    def isValidStopStatement(self, strLine, debug = False):
        state = 1
        table = [
        #    0  1  2
            [0, 2, 0], # STOP
            [0, 0, 0] # Others
        ]
        terms = re.split(' ',strLine)
        finalStates = [ 2 ]
        deadStates = [ 0 ]
        mySwitcher = {
            self.Code.STOP: 0
        }
        return self.validate(terms,state,finalStates, deadStates, table, mySwitcher, None, debug, 1)

    def isValidWhileStatement(self, strLine, debug = False):
        terms = self.removeGarbageFromArray(re.split('(WHILE)',strLine))
        if(len(terms) != 2):
            return False
        if(terms[0] != "WHILE"):
            return False
        if(terms[1][0] != "(" or terms[1][-1] != ")"):
            return False
        return self.isValidBooleanOperation(terms[1],debug)

    def isValidIFstatement(self, strLine, debug = False):
        terms = self.removeGarbageFromArray(re.split('(IF)',strLine))
        if(len(terms) != 2):
            return False
        if(terms[0] != "IF"):
            return False
        if(terms[1][0] != "(" or terms[1][-1] != ")"):
            return False
        return self.isValidBooleanOperation(terms[1],debug) or self.isValidArithmeticOperation(terms[1],debug)

    def inValidINPUTStatement(self, strline, debug = False):
        state = 1
        table = [
        #    0, 1, 2, 3, 4
            [0, 2, 0, 0, 0], # OUTPUT
            [0, 0, 3, 0, 3], # Identifier
            [0, 0, 0, 4, 0], # Comma
            [0, 0, 0, 0, 0] # Others
        ]
        terms = self.removeGarbageFromArray(re.split('(INPUT:)|(,)',strline))
        print(terms)
        othersInput = 5
        finalStates = [ 3 ]
        deadStates = [ 0 ]
        mySwitcher = {
            self.Code.INPUT: 0,
            self.Code.IDENTIFIER: 1,
            self.Code.COMMA: 2
        }
        return self.validate(terms,state,finalStates, deadStates, table, mySwitcher, None, debug, othersInput)

    def isValidOutputStatement(self, strLine, debug = False):
        state = 1
        table = [
        #    0, 1, 2, 3, 4
            [0, 2, 0, 0, 0], # OUTPUT
            [0, 0, 3, 0, 3], # Identifier
            [0, 0, 3, 0, 3], # String Literal
            [0, 0, 0, 4, 0], # Concatenator
            [0, 0, 3, 0, 3], # New Line
            [0, 0, 0, 0, 0] # Others
        ]
        terms = self.removeGarbageFromArray(re.split('(OUTPUT:)|(&)',strLine))
        othersInput = 5
        finalStates = [ 3 ]
        deadStates = [ 0 ]
        mySwitcher = {
            self.Code.OUTPUT: 0,
            self.Code.IDENTIFIER: 1,
            self.Code.STRING_CONST: 2,
            self.Code.CONCATENATOR: 3,
            self.Code.NEWLINE: 4
        }
        return self.validate(terms,state,finalStates, deadStates, table, mySwitcher, None, debug, othersInput)

    def isValidBooleanOperation(self, strLine, debug = False):
        stack = []
        eqTerms = re.split('(\()|(\))|(\=\=)|(\<\=)|(\>\=)|(\&\&)|(\|\|)|(\<)|(\>)|(\+)|(\/)|(\-)|(\*)|(\()|(\))',strLine)
        eqTerms = self.removeGarbageFromArray(eqTerms)
        print(strLine,'TERMS',eqTerms)
        if "=" in eqTerms:
            return False
        nodeList = []
        for elem in eqTerms:
            if(self.isArithmeticOperator(elem)):
                return False
            temp = self.Node(elem)
            nodeList.append(temp)
        length = len(nodeList)
        newNode = self.nodeCreate(nodeList,["==","<=",">=","<",">","&&","||"])
        return self.inorderTraverse(newNode) != None

    def isValidArithmeticOperation(self, strLine, debug = False):
        stack = []
        eqTerms = re.split(' |(\+)|(\/)|(\-)|(\*)|(\%)|(\()|(\))',strLine)
        eqTerms = self.removeGarbageFromArray(eqTerms)
        nodeList = []
        for elem in eqTerms:#strLine.split():
            temp = self.Node(elem)
            nodeList.append(temp)
        length = len(nodeList)
        try:
            newNode = self.nodeCreate(nodeList)
            return self.inorderTraverse(newNode) != None
        except:
            return False
    
    def isValidAssignmentStatement(self, strLine, debug = False):
        state = 1
        table = [
        #    0  1  2  3  4
            [0, 2, 0, 4, 0], # identifier
            [0, 0, 3, 0, 3] # =
        ]
        terms = re.split(' |(\=\=)|(\=)', strLine)
        terms = self.removeGarbageFromArray(terms)
        equation = ""
        indexOfEQ = 0
        for i, e in reversed(list(enumerate(terms))):
            if e == "=":
                break
            equation = e + equation
            indexOfEQ = i
        del terms[indexOfEQ:]
        finalStates = [ 3 ]
        deadStates = [ 0 ]
        mySwitcher = {
            self.Code.IDENTIFIER : 0,
            self.Code.EQUAL: 1,
            self.Code.NUMERIC_CONST: 2,
            self.Code.BOOLEAN_CONST: 2,
            self.Code.STRING_CONST: 2,
            self.Code.CHARACTER_CONST: 2
        }
        currentState = self.validate(terms,state,finalStates, deadStates, table, mySwitcher, None, debug, None)
        if currentState:
            try:
                return self.isValidArithmeticOperation(equation)
            except:
                pass
            try:
                return self.isValidBooleanOperation(equation)
            except:
                pass
        return False

    def isELSE(self, strLine):
        return strLine == "ELSE"

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

    def nodeCreate(self,nodeList:[], operationSequence = ['*','/','%','+','-']):
        index = 0
        while index < len(nodeList):
            if (nodeList[index].value == '('):
                pairIndex= self.findPair(nodeList[index:],index)
                removedList = nodeList[index:pairIndex+1]
                del removedList[0]
                del removedList[-1]
                node = self.nodeCreate(removedList)
                del nodeList[index:pairIndex+1]
                node.value = "TEMP" # simulate SOLVED INPUT
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
        return nodeList[0]


    def inorderTraverse(self,node):
        strRet = ""
        if node == None:
            return
        if node.left != None:
            strRet += self.inorderTraverse(node.left)
        strRet += node.value
        if node.right != None:
            strRet += self.inorderTraverse(node.right)
        return strRet

    # PARSERS

    def isValidIdentifier(self, str):
        state = 1
        table = [
        #    0  1  2
            [0, 2, 2], # _
            [0, 2, 2], # A-Z
            [0, 0, 2], # 0 - 9
            [0, 0, 0]  # Others
        ]
        finalStates = [ 2 ]
        deadStates = [ 0 ]
        mySwitcher = {
            self.charParser.Code.UNDERSCORE: 0,
            self.charParser.Code.LETTER: 1,
            self.charParser.Code.DIGIT: 2
        }
        return self.validate(str, state, finalStates, deadStates, table, mySwitcher, self.charParser)
    
    def isValidStringConstant(self, str, debug = False):
        state = 1
        table = [
        #    0  1  2, 3, 4, 5
            [0, 2, 3, 0, 5, 0], # "
            [0, 0, 4, 0, 5, 0], # [
            [0, 0, 0, 0, 0, 2], # ]
            [0, 0, 2, 0, 0, 0], # Digit
            [0, 0, 2, 0, 0, 0], # Letter
            [0, 0, 2, 0, 5, 0], # Any
        ]
        anyState = 5
        finalStates = [ 3 ]
        deadStates = [ 0 ]
        mySwitcher = {
            self.charParser.Code.QUOTE: 0,
            self.charParser.Code.OSQRBK: 1,
            self.charParser.Code.CSQRBK: 2,
            self.charParser.Code.DIGIT: 3,
            self.charParser.Code.LETTER: 4
        }
        return self.validate(str, state, finalStates, deadStates, table, mySwitcher, self.charParser, debug, anyState)

    def isValidNumericConstant(self, str, debug = False):
        state = 1
        table = [
        #    0  1  2, 3, 4
            [0, 2, 2, 4, 4], # Digit
            [0, 3, 3, 0, 0], # dot
            [0, 0, 0, 0, 0], # Any
        ]
        anyState = 5
        finalStates = [ 2, 4 ]
        deadStates = [ 0 ]
        mySwitcher = {
            self.charParser.Code.DIGIT: 0,
            self.charParser.Code.DOT: 0,
        }
        return self.validate(str, state, finalStates, deadStates, table, mySwitcher, self.charParser, debug, anyState)

    def isValidCharacterConstant(self, str, debug = False):
        state = 1
        table = [
        #    0  1  2, 3, 4, 5, 6
            [0, 2, 3, 0, 5, 0, 3], # '
            [0, 0, 4, 0, 5, 0, 0], # [
            [0, 0, 0, 0, 0, 6, 0], # ]
            [0, 0, 6, 0, 0, 0, 0], # Digit
            [0, 0, 6, 0, 0, 0, 0], # Letter
            [0, 0, 6, 0, 5, 0, 0], # Any
        ]
        anyState = 5
        finalStates = [ 3 ]
        deadStates = [ 0 ]
        mySwitcher = {
            self.charParser.Code.SINGLE_QUOTE: 0,
            self.charParser.Code.OSQRBK: 1,
            self.charParser.Code.CSQRBK: 2,
            self.charParser.Code.DIGIT: 3,
            self.charParser.Code.LETTER: 4
        }
        return self.validate(str, state, finalStates, deadStates, table, mySwitcher, self.charParser, debug, anyState)

    def isValidBooleanConstant(self, str, debug = False):
        return str == "FALSE" or str == "TRUE"
    # KEYWORDS

    def isValidVAR(self, str):
        return str == "VAR"

    def isValidAS(self, str):
        return str == "AS"
    
    def isValidDataType(self, str):
        return self.isIntDataType(str) | self.isCharDataType(str) | self.isBoolDataType(str) | self.isFloatDataType(str)
    
    def isIntDataType(self, str):
        return str == "INT"
    
    def isCharDataType(self, str):
        return str == "CHAR"
    
    def isBoolDataType(self, str):
        return str == "BOOL"
    
    def isFloatDataType(self, str):
        return str == "FLOAT"
    
    def isStart(self, str):
        return str == "START"
    
    def isStop(self, str):
        return str == "STOP"

    def isOutput(self, str):
        return str == "OUTPUT:"

    def isInput(self, str):
        return str == "INPUT:"

    def isANDOperator(self, str):
        return str == "AND"

    def isOROperator(self, str):
        return str == "OR"
    
    def isNOTOperator(self, str):
        return str == "NOT"

    def isCommentOperator(self, str):
        if len(str) != 1:
            return False
        return self.charParser.isMultiplySign(str[0])

    def isArithmeticOperator(self, str):
        code  = self.charParser.getCode(str)
        opSwitcher = {
            self.charParser.Code.PLUS: True,
            self.charParser.Code.MINUS: True,
            self.charParser.Code.DIVIDE: True,
            self.charParser.Code.MULTIPLY: True,
            self.charParser.Code.MODULO: True
        }
        # print(opSwitcher.get(code,False))
        return opSwitcher.get(code,False)

    def isBooleanOperator(self, str):
        code = self.charParser.getCode(str)
        opSwitcher = {
            self.charParser.Code.EQEQ: True,
            self.charParser.Code.LTEQ: True,
            self.charParser.Code.LT: True,
            self.charParser.Code.GT: True,
            self.charParser.Code.GTEQ: True,
            self.charParser.Code.AND: True,
            self.charParser.Code.OR: True
        }
        return opSwitcher.get(code,False)

    def isNewLine(self, str):
        return True if (len(str) == 1) & (self.charParser.getCode(str[0]) == self.charParser.Code.SHARP) else False

    def isConcatenator(self, str):
        return True if (len(str) == 1) & (self.charParser.getCode(str[0]) == self.charParser.Code.AMPERSAND) else False

    def isIF(self, str):
        return str == "IF"

    def removeGarbageFromArray(str, terms, strip = True):
        terms = [x for x in terms if x is not None]
        terms = [x for x in terms if x is not ' ']
        terms = [x for x in terms if x is not '']
        if(strip):
            terms = [x.strip() for x in terms]
        return terms


    def isKeyWord(self, str):
        code = self.getCode(str)
        mySwitcher = {
            self.Code.VAR: 0,
            self.Code.AS: 1,
            self.Code.START: 2,
            self.Code.STOP: 3,
            self.Code.DATA_TYPE: 4,
            self.Code.OUTPUT: 5
        }
        code = mySwitcher.get(code, -1)
        return code != -1

    def getCode(self, str):
        # KEYWORDS
        if(self.isValidVAR(str)):
            return self.Code.VAR
        if(self.isValidAS(str)):
            return self.Code.AS
        if(self.isStart(str)):
            return self.Code.START
        if(self.isStop(str)):
            return self.Code.STOP
        if(self.isValidDataType(str)):
            return self.Code.DATA_TYPE
        if(self.isOutput(str)):
            return self.Code.OUTPUT
        if(self.isInput(str)):
            return self.Code.INPUT
        if(self.isIF(str)):
            return self.Code.IF
        if(self.isELSE(str)):
            return self.Code.ELSE
        # Dynamice
        if(self.isValidIdentifier(str)):
            return self.Code.IDENTIFIER
        if(self.isValidStringConstant(str)):
            return self.Code.STRING_CONST
        if(self.isValidNumericConstant(str)):
            return self.Code.NUMERIC_CONST
        if(self.isValidBooleanConstant(str)):
            return self.Code.BOOLEAN_CONST
        if(self.isValidCharacterConstant(str)):
            return self.Code.CHARACTER_CONST
        # characters
        if(self.charParser.isEqualSign(str)):
            return self.Code.EQUAL
        if(self.charParser.isComma(str)):
            return self.Code.COMMA
        if(self.isCommentOperator(str)):
            return self.Code.COMMENT_OP
        if(self.isConcatenator(str)):
            return self.Code.CONCATENATOR
        if(self.isNewLine(str)):
            return self.Code.NEWLINE
        if(self.isArithmeticOperator(str)):
            return self.Code.ARITHMETIC_OP
        return self.Code.ERROR
