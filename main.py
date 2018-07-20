from parser import CharacterParser
from interpreter import Interpreter


parser = CharacterParser()
interpreter = Interpreter()

str = ','
# print(str, ':', interpreter.isValidIdentifier(str))
# str = 'VAR abc, abcd AS INT'
# print(str, ':', interpreter.isValidInitializationStatement(str))
# str = '* this is a comment'
# print(str, ':', interpreter.isValidCommentStatement(str))
str = 'START'
print(str, ':', interpreter.isValidStartStatement(str))
str = 'STOP'
print(str, ':', interpreter.isValidStopStatement(str))
# str = 'abd1'
# print(str, ':', interpreter.isValidIdentifier(str))
# str = '1abc'
# print(str, ':', interpreter.isValidIdentifier(str))
# str = '_abc'
# print(str, ':', interpreter.isValidIdentifier(str))
# str = '__'
# print(str, ':', interpreter.isValidIdentifier(str))