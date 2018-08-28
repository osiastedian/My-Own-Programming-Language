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
        STRING = 11
        ARITHMETIC_OP = 12
        NUMERIC_CONST = 13

    
    def __init__(self):
        self.charParser = CharacterParser()
        self.memory = []
    
    # STATEMENTS
    def validate(self, terms, startState, finalStates, deadStates, table, switcher, coder = None, debug = False, anyInputCode = -1):
        if(debug):
            print(terms)
        state = startState
        for term in terms:
            if((term is not None) & (term is not '')):
                if(coder is None):
                    code = self.getCode(term)
                else:
                    code = coder.getCode(term)
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
            [0, 0, 0, 0, 5, 0]  # Data Type
        ]
        terms = re.split(' |(\,)', strLine)
        finalStates = [ 5 ]
        deadStates = [ 0 ]
        mySwitcher = {
            self.Code.VAR: 0,
            self.Code.IDENTIFIER : 1,
            self.Code.COMMA: 2,
            self.Code.AS: 3,
            self.Code.DATA_TYPE: 4
        }
        return self.validate(terms,state,finalStates, deadStates, table, mySwitcher, None, debug, None)
        
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
        terms = re.split(' ',strLine)
        othersInput = 5
        finalStates = [ 3 ]
        deadStates = [ 0 ]
        mySwitcher = {
            self.Code.OUTPUT: 0,
            self.Code.IDENTIFIER: 1,
            self.Code.STRING: 2,
            self.Code.CONCATENATOR: 3,
            self.Code.NEWLINE: 4
        }
        return self.validate(terms,state,finalStates, deadStates, table, mySwitcher, None, debug, othersInput)

    def isValidArithmeticOperation(self, strLine, debug = False):
        stack = []
        strLine = strLine.replace('(',' ( ')
        strLine = strLine.replace(')',' ) ')
        strLine = strLine.replace('+',' + ')
        strLine = strLine.replace('-',' - ')
        strLine = strLine.replace('/',' / ')
        strLine = strLine.replace('*',' * ')
        nodeList = []
        for elem in strLine.split():
            temp = self.Node(elem)
            nodeList.append(temp)
        length = len(nodeList)
        
        while len(nodeList) != 1:
            index = 0
            while index < len(nodeList):
                if(self.isArithmeticOperator(nodeList[index].value)):
                    nodeList[index].right = nodeList[index+1]
                    nodeList[index].left = nodeList[index-1]
                    del nodeList[index+1]
                    del nodeList[index-1]
                    continue
                index = index + 1
        # print('Final:',nodeList)
        self.inorder(nodeList[0])
        # print(strLine.split())
    
    def inorder(self, t):
        if t is not None:
            self.inorder(t.left)
            print (t.value),
            self.inorder(t.right)

    def isValidBooleanExpression(self, strLine, debug = False):
        return
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
    
    def isValidString(self, str, debug = False):
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
            self.charParser.Code.MULTIPLY: True
        }
        # print(opSwitcher.get(code,False))
        return opSwitcher.get(code,False)

    def isNewLine(self, str):
        return True if (len(str) == 1) & (self.charParser.getCode(str[0]) == self.charParser.Code.SHARP) else False

    def isConcatenator(self, str):
        return True if (len(str) == 1) & (self.charParser.getCode(str[0]) == self.charParser.Code.AMPERSAND) else False

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
        # Dynamice
        if(self.isValidIdentifier(str)):
            return self.Code.IDENTIFIER
        if(self.isValidString(str)):
            return self.Code.STRING
        if(self.isValidNumericConstant(str)):
            return self.Code.NUMERIC_CONST
        # characters
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
    