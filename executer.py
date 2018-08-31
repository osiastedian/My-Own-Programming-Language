from interpreter import Interpreter
from enum import Enum
class Executer:

    class Statment:
        def __init__(self, code : int = -1, line: str = ""):
            self.code = code  
            self.line = line

    class Code(Enum):
        ERROR = -1
        INIT_STATEMENT = 0
        COMMENT_STATEMENT = 1
        START_STATEMENT = 2
        STOP_STATEMENT = 3
        OUTPUT_STATEMENT = 4
        ASSIGNMENT_STATEMENT = 5
        

    def __init__(self):
        self.interpreter = Interpreter()
        self.parsed = []
        self.memory = []
    
    def executeProgram(self, strLines):
        for line in strLines:
            stmt = self.Statment(self.getCode(line), line)
            self.parsed.append(stmt)
        for stmt in self.parsed:
            print('Code:', stmt.code,'\t\t=',stmt.line)
    
    def getCode(self, strLine):
        if(self.interpreter.isValidInitializationStatement(strLine)):
            return self.Code.INIT_STATEMENT
        if(self.interpreter.isValidCommentStatement(strLine)):
            return self.Code.COMMENT_STATEMENT
        if(self.interpreter.isValidStartStatement(strLine)):
            return self.Code.START_STATEMENT
        if(self.interpreter.isValidStopStatement(strLine)):
            return self.Code.STOP_STATEMENT
        if(self.interpreter.isValidOutputStatement(strLine)):
            return self.Code.OUTPUT_STATEMENT
        if(self.interpreter.isValidAssignmentStatement(strLine)):
            return self.Code.ASSIGNMENT_STATEMENT
        return self.Code.ERROR


exec = Executer()

strLines = [
'* my first program in CFPL',
'VAR abc, b, c AS INT',
'VAR x, w_23=’w’ AS CHAR',
'VAR t=”TRUE” AS BOOL',
'START',
'abc=b=10',
'w_23=’a’',
'* this is a comment',
'OUTPUT: abc & "hi" & b & "#" & w_23 & "[#]"',
'STOP'
]

exec.executeProgram(strLines)
