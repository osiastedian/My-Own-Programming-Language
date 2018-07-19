
from enum import Enum

class CharacterParser:

    class Code(Enum):
        ERROR = -1
        DIGIT = 0
        LETTER = 1
        UNDERSCORE = 2
        EQUAL = 3
        ADD = 4
        MINUS = 5
        DIVIDE = 6
        MULTIPLY = 7
        COMMA = 8

    def isDigit(self, char):
        num = ord(char)
        return  num >= ord('0') | num <= ord('9')
    
    def isLetter(self, char):
        return self.isUpperCase(char) | self.isLowerCase(char)

    def isUpperCase(self, char):
        num = ord(char)
        return num >= ord('A') & num <= ord('Z')
    
    def isLowerCase(self, char):
        num = ord(char)
        return num >= ord('a') & num <= ord('z')
    
    def isUnderscore(self, char):
        return char == '_'
    
    def isEqualSign(self, char):
        return char == '='
    
    def isAddSign(self, char):
        return char == '+'
    
    def isMinusSign(self, char):
        return char == '-'
    
    def isMultiplySign(self, char):
        return char == '*'
    
    def isDivideSign(self, char):
        return char == '/'

    def isComma(self, char):
        return char == ','
    
    def getCode(self, str):
        if(self.isDigit(str)):
            return self.Code.DIGIT
        if(self.isLetter(str)):
            return self.Code.LETTER
        if(self.isUnderscore(str)):
            return self.Code.UNDERSCORE
        if(self.isEqualSign(str)):
            return self.Code.EQUAL
        if(self.isAddSign(str)):
            return self.Code.ADD
        if(self.isMinusSign(str)):
            return self.Code.MINUS
        if(self.isMultiplySign(str)):
            return self.Code.MULTIPLY
        if(self.isDivideSign(str)):
            return self.Code.DIVIDE
        if(self.isComma(str)):
            return self.Code.COMMA
        return self.Code.ERROR
        