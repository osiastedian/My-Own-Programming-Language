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
    
    def __init__(self):
        self.charParser = CharacterParser()
        self.memory = []
        
    def validate(self, terms, startState, finalStates, deadStates, table, switcher, coder = None, debug = False):
        if(debug):
            print(terms)
        state = startState
        for term in terms:
            if((term is not None) & (term is not '')):
                if(coder is None):
                    code = self.getCode(term)
                else:
                    code = coder.getCode(term)
                code = switcher.get(code, 3)
                if(debug):
                    print('TERM', term, 'state: ', state, 'code: ', code)
                state = table[code][state]
                if(debug & (state in deadStates)):
                    print(term, 'is DEAD code:', code)
                    break
        return state in finalStates

    def isValidInitialization(self, strLine, debug = False):
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
        return self.validate(terms,state,finalStates, deadStates, table, mySwitcher)
        

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
    
    def getCode(self, str):
        if(self.isValidVAR(str)):
            return self.Code.VAR
        if(self.isValidAS(str)):
            return self.Code.AS
        if(self.isValidDataType(str)):
            return self.Code.DATA_TYPE
        if(self.isValidIdentifier(str)):
            return self.Code.IDENTIFIER
        if(self.charParser.isComma(str)):
            return self.Code.COMMA
        return self.Code.ERROR
    