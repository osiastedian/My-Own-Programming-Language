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
        

    def isValidAssignmentOperation(self, strLine):
        state = 1
        table = [
        #    0  1  2  3  4  5
            [0, 2, 0, 0, 0, 0], # VAR
            [0, 0, 3, 0, 0, 0], # identifier
            [0, 0, 0, 2, 0, 0], # COMMA
            [0, 0, 0, 4, 0, 0], # AS
            [0, 0, 0, 0, 5, 0]  # Data Type
        ]
        terms = re.split(' |\,', strLine)

    def isValidIdentifier(self, str):
        state = 1
        finalStates = [ 2 ]
        table = [
        #    0  1  2
            [0, 2, 2], # _
            [0, 2, 2], # A-Z
            [0, 0, 2], # 0 - 9
            [0, 0, 0]  # Others
        ]
        mySwitcher = {
            self.charParser.Code.UNDERSCORE: 0,
            self.charParser.Code.LETTER: 1,
            self.charParser.Code.DIGIT: 2
        }
        for ch in str:
            code = self.charParser.getCode(ch)
            code = mySwitcher.get(code, 3)
            state = table[code][state]
        return state in finalStates
    
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
    
    