from parser import CharacterParser
from interpreter import Interpreter


parser = CharacterParser()
interpreter = Interpreter()

str = 'abd1'
print(str, ':', interpreter.isValidIdentifier(str))
str = '1abc'
print(str, ':', interpreter.isValidIdentifier(str))
str = '_abc'
print(str, ':', interpreter.isValidIdentifier(str))
str = '__'
print(str, ':', interpreter.isValidIdentifier(str))