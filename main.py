import math, string
from funcs import *

def openFile(name):
    with open(name, encoding='utf-8') as file:
        fileText = file.read().split("\n")
    return fileText

def writeToFile(name, data):
    with open(name,'w', encoding='utf-8') as file:
        file.write(data)

# Place inverse functions before normal versions
global written_operators
written_operators = ["²", "sin⁻¹", "cos⁻¹", "√", "sqrt", "remainder", "sin", "cos", "round"]
keywords = ["Prompt", "While", "If", "Then", "Else", "End", "Disp"]

# Watch out for a line like `Asqrt(B)->C`
def parse(line):
    # How to tell a token?
    # Types of tokens
    # - String literals - Quotes around
    # - Keywords - Capital first, then rest lowercase [only at beginning of line]
    # - Numeric literals - Digits, decimal point
    # - Operators - Symbols or all lowercase
    # - Variables - Capital letters only
    tokens = []
    tokenType = None
    skipCounter = 0
    if not line or line[0] == '#': return [] # Provide for commenting with pound sign
    # TODO: Strip whitespace before checks
    for i, char in enumerate(line):
        if skipCounter: # If a keyword is matched
            skipCounter -= 1
            continue
        elif tokenType == "String": # If a string is currently being parsed, add to that string
            tokens[-1][0] += char
            if char == "\"": # Finish a string
                tokenType = None
        elif char == "\"": # Begin a string
            tokens.append([char, "String"])
            tokenType = "String"
        elif char in string.ascii_uppercase or char == 'θ':
            tokens.append([char, "Variable"])
            tokenType = "Uppercase"
        elif char in string.ascii_lowercase or char in '√²':
            op_match = 0
            kw_match = 0
            for op in written_operators: # Check for written operator match
                if line[i:i+len(op)] == op:
                    skipCounter = len(op) if op != '²' else 0
                    tokens.append([op, "Operator"])
                    tokenType = None
                    op_match = 1
                    break
            if op_match: continue
            if tokenType == "Uppercase":
                for keyword in keywords:
                    if line[i-1:i+len(keyword)-1] == keyword:
                        skipCounter = len(keyword)-1
                        tokens[-1] = [keyword, "Keyword"]
                        tokenType = None
                        kw_match = 1
                        break
            if kw_match: continue
        elif char in string.digits + '.': # Check for number or decimal point
            if tokenType == "Number":
                tokens[-1][0] += char
            else:
                tokens.append([char, "Number"])
                tokenType = "Number"
        else: # This should include all operators
            tokenType = "Operator"
            if char == ">" and tokens[-1][0] == "-": # Variable assignment
                tokens[-1][0] += char
                tokens[-1][1] = "Assignment"
            elif char in "<=>":
                if tokens[-1][0] in "<>!": # Inequalities
                    tokens[-1][0] += char
                    tokens[-1][1] = "Comparator"
                else:
                    tokens.append([char, "Comparator"])
            else:
                tokens.append([char, "Operator"])
    return tokens

def addLines(python, indents, content):
    python.extend([' ' * 4 * indents + x for x in content])

# Compiling the TI-BASIC to a native Python file
# NOTE: This overwrites the default `compile` function in Python
# Example: `compile('test/ARMY.8XP','test/ARMY.py')`
def compile(name, outputName=''):
    python = ['from math import *',
                      'def disp(*args):', # Remove decimal points from integers when printing
                      '        print(" ".join(str(int(arg) if type(arg) == float and arg % 1 == 0 else arg) for arg in args))\n']
    fileText = openFile(name)
    indents = 0
    ifStmt = 0
    block = 0
    for line in fileText:
        if ifStmt in (1, 2): # Clock to see whether `if` is expression or block
            ifStmt -= 1
        tokens = parse(line)
        if not tokens: continue
        #print(tokens)
        if tokens[0][1] == "Keyword":
            kw = tokens[0][0]
            if kw == "Prompt":
                addLines(python, indents, Prompt(tokens))
            elif kw == "If":
                addLines(python, indents, If(tokens))
                ifStmt = 2
                indents += 1
            elif kw == "While":
                addLines(python, indents, While(tokens))
                indents += 1
                block += 1
            elif kw == "Else":
                if not block: # `else` without an `if`
                    # TODO: Better detection to ensure `while` does not satisfy `else`
                    raise SyntaxError
                addLines(python, indents-1, Else(tokens))
            elif kw == "Disp":
                addLines(python, indents, Disp(tokens))
            elif kw == "Then":
                if ifStmt: # This is now an if-block, not a single expression
                    block += 1
                else: # `then` without an `if`
                    raise SyntaxError
            elif kw == "End":
                indents -= 1
                if block:
                    block -= 1
                else: # `end` without a loop or conditional
                    raise SyntaxError
        elif tokens[-2][1] == 'Assignment': # Statement contains assignment
            addLines(python, indents, Assign(tokens))
        elif 'Keyword' in (token[1] for token in tokens):
            raise SyntaxError
        else:
            addLines(python, indents, Pass(tokens))
        # Gather all lines, then figure out tabs from scope and `End`s
    out = '\n'.join(python)
    if outputName:
        writeToFile(outputName, out)
    print('\nOUTPUT:\n\n'+out)

# If return value, print that value
#       Values are returned by evaluating or assigning expressions as the final
#       statement in a program
# Else, print "Done"
