from parser import CharacterParser
from interpreter import Interpreter


parser = CharacterParser()
interpreter = Interpreter()

# str = 'abcd = 1'
# print(str, interpreter.isValidAsignmentStatement(str))
str = 'a + b + 123'
print(str, interpreter.isValidArithmeticOperation(str, True))
# str = '123'
# print(str, interpreter.isValidNumericConstant(str, True))

# str = 'OUTPUT: abcd & "Hello[?]" & # & "[[]"'
# print(str, interpreter.isValidOutputStatement(str))
# str = 'a'
# print(str, parser.isSpecialChar(str))

# str = '"[a]"'
# print(str, interpreter.isValidString(str, True))
# str = '#'
# print(str, interpreter.isNewLine(str))
# print(str, ':', interpreter.isValidIdentifier(str))
# str = 'VAR abc, abcd AS INT'
# print(str, ':', interpreter.isValidInitializationStatement(str))
# str = '* this is a comment'
# print(str, ':', interpreter.isValidCommentStatement(str))
# str = 'START'
# print(str, ':', interpreter.isValidStartStatement(str))
# str = 'STOP'
# print(str, ':', interpreter.isValidStopStatement(str))
# str = 'abd1'
# print(str, ':', interpreter.isValidIdentifier(str))
# str = '1abc'
# print(str, ':', interpreter.isValidIdentifier(str))
# str = '_abc'
# print(str, ':', interpreter.isValidIdentifier(str))
# str = '__'
# print(str, ':', interpreter.isValidIdentifier(str))