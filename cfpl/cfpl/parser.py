from enum import Enum

class CharacterParser:

    class Code(Enum):
        ERROR = -1
        DIGIT = 0
        LETTER = 1
        UNDERSCORE = 2
        EQUAL = 3
        PLUS = 4
        MINUS = 5
        DIVIDE = 6
        MULTIPLY = 7
        COMMA = 8
        AMPERSAND = 9
        GT = 10
        LT = 11
        GTEQ = 12
        LTEQ = 13
        EQEQ = 14
        NTEQ = 15
        QUOTE = 16
        OSQRBK = 17
        CSQRBK = 18
        SPECIAL = 19
        SHARP = 20
        DOT = 21
        SINGLE_QUOTE = 22
        AND = 23
        OR = 24
        MODULO = 25

    def isDigit(self, char):
        num = ord(char)
        return  num >= ord('0') | num <= ord('9')
    
    def isLetter(self, char):
        return self.isUpperCase(char) | self.isLowerCase(char)

    def isUpperCase(self, char):
        num = ord(char)
        return (num >= ord('A')) & (num <= ord('Z'))
    
    def isLowerCase(self, char):
        num = ord(char)
        return (num >= ord('a')) & (num <= ord('z'))
    
    def isUnderscore(self, char):
        return char == '_'
    
    def isEqualSign(self, char):
        return char == '='
    
    def isPlusSign(self, char):
        return char == '+'
    
    def isMinusSign(self, char):
        return char == '-'
    
    def isMultiplySign(self, char):
        return char == '*'
    
    def isDivideSign(self, char):
        return char == '/'

    def isComma(self, char):
        return char == ','
    
    def isAmpersand(self, char):
        return char == '&'
    
    def isGTSign(self, char):
        return char == '>'
    
    def isLTSign(self, char):
        return char == '<'
    
    def isLTEQSign(self, char):
        return char == '<='
    
    def isGTEQSign(self, char):
        return char == '>='
    
    def isEQEQSign(self, char):
        return char == '=='

    def isNTEQSign(self, char):
        return char == '<>'
    
    def isQuoteSign(self, char):
        return char == '\"'
    
    def isOpenSqrBracket(self, char):
        return char == '['
    
    def isCloseSqrBracket(self, char):
        return char == ']'
    
    def isSpecialChar(self, char):
        return not (self.isLetter(char) | self.isDigit(char))

    def isSharpSign(self, char):
        return char == '#'

    def isDOTSign(self, char):
        return char == '.'
    
    def isSingleQuote(self, char):
        return char == '\''

    def isBooleanANDOperator(self, str):
        return str == "&&"
    
    def isBooleanOROperator(self, str):
        return str == "||"
    
    def isModuloOperator(self, str):
        return str == "%"

    def getCode(self, str):
        if(self.isGTSign(str)):
            return self.Code.GT
        if(self.isGTEQSign(str)):
            return self.Code.GTEQ
        if(self.isLTSign(str)):
            return self.Code.LT
        if(self.isLTEQSign(str)):
            return self.Code.LTEQ
        if(self.isEQEQSign(str)):
            return self.Code.EQEQ
        if(self.isNTEQSign(str)):
            return self.Code.NTEQ
        if(len(str) > 1):
            return self.Code.ERROR
        if(self.isDigit(str)):
            return self.Code.DIGIT
        if(self.isLetter(str)):
            return self.Code.LETTER
        if(self.isUnderscore(str)):
            return self.Code.UNDERSCORE
        if(self.isEqualSign(str)):
            return self.Code.EQUAL
        if(self.isPlusSign(str)):
            return self.Code.PLUS
        if(self.isMinusSign(str)):
            return self.Code.MINUS
        if(self.isMultiplySign(str)):
            return self.Code.MULTIPLY
        if(self.isDivideSign(str)):
            return self.Code.DIVIDE
        if(self.isComma(str)):
            return self.Code.COMMA
        if(self.isAmpersand(str)):
            return self.Code.AMPERSAND
        if(self.isQuoteSign(str)):
            return self.Code.QUOTE
        if(self.isOpenSqrBracket(str)):
            return self.Code.OSQRBK
        if(self.isCloseSqrBracket(str)):
            return self.Code.CSQRBK
        if(self.isSharpSign(str)):
            return self.Code.SHARP
        if(self.isDOTSign(str)):
            return self.Code.DOT
        if(self.isSingleQuote(str)):
            return self.Code.SINGLE_QUOTE
        if(self.isModuloOperator(str)):
            return self.Code.MODULO
        if(self.isSpecialChar(str)):
            return self.Code.SPECIAL
        
        return self.Code.ERROR

p = CharacterParser()
        