class ArgumentError(Exception):
    __module__ = 'builtins'

def translateExp(tokens): # Translate literals and operators
    from main import written_operators
    # This function is not responsible for ArgumentErrors
    newTokens = []
    op = 1
    comp = 0
    skipCounter = 0
    coeff = False
    for i, token in enumerate(tokens):
        if skipCounter:
            skipCounter -= 1
            continue
        if token[1] in ['Comparator', 'Number', 'String', 'Variable']:
            newTokens.append(token[0]) # Literals are directly translated
            #print(token, newTokens, coeff)
            if coeff:
                if token[1] == 'Variable':
                    newTokens.insert(-1, '*')
                elif token[1] == 'String':
                    raise SyntaxError # Trying to multiply strings, are we?
            elif token[1] in ['Number', 'Variable']:
                coeff = True
            else:
                coeff = False
                if token[1] == 'Comparator':
                    if comp: raise SyntaxError # Consecutive comparators
                    else: comp = 1
                    if token[0] == '=': newTokens[-1] += '=' # Double equals sign
                elif comp or op:
                    comp = 0
                    op = 0
                else:
                    raise SyntaxError # Adjacent literals
        elif token[1] == "Operator":
            op = 1
            opWord = token[0]
            tokenContents = [token[0] for token in tokens]
            if opWord in ',/*-+':
                newTokens.append(token[0])
            else:
                if opWord == '²': # TODO: Add arbitrary exponents
                    newTokens.append('**2')
                elif coeff:
                    newTokens.append('*')
                if opWord in ['sin','cos','sqrt','√']:
                    openParen, closeParen = 0, 0
                    parenIndex = -1
                    for charIndex, char in enumerate(tokenContents[i+1:]):
                        #print('iter', openParen, closeParen, charIndex, char)
                        if char == '(' or char in written_operators[1:]: openParen += 1
                        elif char == ')': closeParen += 1
                        if closeParen > openParen:
                            parenIndex = charIndex+1
                            break
                    skipCounter = parenIndex
                    if opWord == '√':
                        opWord = 'sqrt'
                    newTokens.append(opWord+'('+''.join(translateExp(tokens[i+1:i+parenIndex]))+')') 
                elif opWord in ['remainder', 'round']:
                    commaIndex = -1
                    openParen, closeParen = 0, 0
                    parenIndex = -1
                    for charIndex, char in enumerate(tokenContents[i+1:]):
                        #print('iter', openParen, closeParen, charIndex, char)
                        if char == '(' or char in written_operators[1:]: openParen += 1
                        elif char == ',' and openParen == closeParen:
                            if commaIndex < 0:
                                commaIndex = charIndex+1
                            else: # Too many arguments
                                raise SyntaxError
                        elif char == ')': closeParen += 1
                        if closeParen > openParen:
                            parenIndex = charIndex+1
                            break
                    skipCounter = parenIndex
                    parenIndex = len(tokens) if parenIndex < 0 else parenIndex
                    #print('FULL TOKENS WITH INDICES:', tokens, i, commaIndex, parenIndex)
                    precomma = translateExp(tokens[i+1:i+commaIndex])
                    postcomma = translateExp(tokens[i+commaIndex+1:parenIndex])
                    #print('PRECOMMA', precomma, '\nPOSTCOMMA', postcomma)
                    if commaIndex == -1:
                        raise ArgumentError # Not enough arguments
                    if opWord == 'remainder': 
                        newTokens.append(''.join(precomma) + ' % ' + ''.join(postcomma))
                    else:
                        newTokens.append('round('+''.join(precomma) + ', ' + ''.join(postcomma)+')')
            coeff = False
        else:
            raise SyntaxError # Undefined behavior
    return newTokens

def Prompt(tokens):
    newLines = []
    comma = 1
    if len(tokens) < 2: # Not enough arguments
        raise ArgumentError
    for token in tokens[1:]:
        if token[0] == ",":
            if comma: # Out-of-place commas
                raise SyntaxError
            else:
                comma = 1
        elif comma:
            if token[1] == "Variable":
                letter = token[0]
                newLines += ['user = float(input("'+letter+'=?"))',
                                        token[0]+'= int(user) if not user % 1 else user']
                comma = 0
            else: # Assigning to a non-variable
                raise SyntaxError
        else: # No commas
            raise SyntaxError
    if comma: # Ends with comma
        raise SyntaxError
    return newLines

def If(tokens):
    if len(tokens) < 2: # Not enough arguments
        raise ArgumentError
    return ['if '+''.join(translateExp(tokens[1:]))+':']

def Else(tokens):
    if len(tokens) > 1:
        raise SyntaxError
    return ['else:']

def While(tokens):
    if len(tokens) < 2: # Not enough arguments
        raise ArgumentError
    return ['while '+''.join(translateExp(tokens[1:]))+':']

def Disp(tokens):
    return ['disp('+''.join(translateExp(tokens[1:]))+')']

def Assign(tokens):
    return [tokens[-1][0]+'='+''.join(translateExp(tokens[:-2]))]

def Pass(tokens):
    return ['pass # '+''.join(translateExp(tokens))]

