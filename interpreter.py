from parser import CharacterParser
import re

from enum import Enum

class Interpreter:

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
        # Dynamice
        if(self.isValidIdentifier(str)):
            return self.Code.IDENTIFIER
        
        # characters
        if(self.charParser.isComma(str)):
            return self.Code.COMMA
        if(self.isCommentOperator(str)):
            return self.Code.COMMENT_OP
        return self.Code.ERROR
    