from parser import CharacterParser
from interpreter import Interpreter
import re

parser = CharacterParser()
interpreter = Interpreter()

# str = "ac = abc == 100 && abc"
str = "100+(3.33*3)"
print(str,interpreter.isValidBooleanOperation(str))
# str = "abc = abc / 4  + (1 - 3) * 4"
# print(str, interpreter.isValidAssignmentStatement(str, True))

# def removeGarbageFromArray(terms, strip = True):
#         terms = [x for x in terms if x is not None]
#         terms = [x for x in terms if x is not ' ']
#         terms = [x for x in terms if x is not '']
#         if(strip):
#             terms = [x.strip() for x in terms]
#         return terms

# def findPair(nodeList: [], index):
#     stack = []
#     retIndex = index
#     for node in nodeList:
#         if(node.value == '('):
#             stack.append(node.value)
#         elif(node.value == ')'):
#             stack.pop()
#         if len(stack) == 0:
#             break
#         retIndex = retIndex + 1
#     return retIndex

# def nodeCreate(nodeList:[]):
#     index = 0
#     while index < len(nodeList):
#         if (nodeList[index].value == '('):
#             pairIndex= findPair(nodeList[index:],index)
#             removedList = nodeList[index:pairIndex+1]
#             del removedList[0]
#             del removedList[-1]
#             node = nodeCreate(removedList)
#             del nodeList[index:pairIndex+1]
#             nodeList.insert(index,node)
#         index = index + 1
#     operationSequenc = ['*','/','+','-']
#     for operation in operationSequenc:
#         index = 0
#         while index < len(nodeList):
#             if(nodeList[index].value == operation):
#                 if(index+1 < len(nodeList)):
#                     nodeList[index].right = nodeList[index+1]
#                     del nodeList[index+1]
#                 if(index-1 >= 0):
#                     nodeList[index].left = nodeList[index-1]
#                     del nodeList[index-1]
#             index = index + 1
#     return nodeList[0]

# def inorderTraverse(node):
#     strRet = ""
#     if node == None:
#         return
#     if node.left != None:
#         strRet += inorderTraverse(node.left)
#     strRet += node.value
#     if node.right != None:
#         strRet += inorderTraverse(node.right)
#     return strRet

# str = "abc / 4  + (1 - 3) * 4"
# terms = re.split(' |(\+)|(\/)|(\-)|(\*)|(\()|(\))',str)
# terms = removeGarbageFromArray(terms)
# nodeList = []
# for term in terms:
#     temp = Interpreter.Node(term)
#     nodeList.append(temp)
# node = nodeCreate(nodeList)
# print(inorderTraverse(node))

# print(node)
# print(str, interpreter.isValidArithmeticOperation(str,True))


# str = 'OUTPUT: "hi"'
# str = 'OUTPUT: abc & "hi" & b & "#" & w_23 & "[#]"'
# print(str, interpreter.isValidOutputStatement(str, True))
# str = '"Hi"'
# print(str, interpreter.getCode(str))
# str = "VAR abcd = 10,bcd = 100 AS INT"
# print(str, interpreter.isValidInitializationStatement(str, True))
# str = 'abc=b=10'
# print(str, interpreter.isValidAssignmentStatement(str, True))
# str = "TRUEa"
# print(str, interpreter.isValidBooleanConstant(str))
# str = "'[#]'"
# print(str, interpreter.isValidCharacterConstant(str))
# str = 'abcd = 1'
# print(str, interpreter.isValidAsignmentStatement(str))
# str = 'a + b + 123'
# print(str, interpreter.isValidArithmeticOperation(str, True))
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