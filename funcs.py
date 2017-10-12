class ArgumentError(Exception):
    __module__ = 'builtins'

def translateExp(tokens): # Translate literals and operators
    # This function is not responsible for ArgumentErrors
    newTokens = []
    op = 0
    comp = 0
    skipCounter = 0
    coeff = False
    for i, token in enumerate(tokens):
        if skipCounter:
            skipCounter -= 1
            continue
        if token[1] in ['Comparator', 'Number', 'String', 'Variable']:
            newTokens.append(token[0]) # Literals are directly translated
            if coeff:
                if token[1] == 'Variable':
                    newTokens.insert(-1, '*')
                elif token[1] == 'String':
                    raise SyntaxError # Trying to multiply strings, are we?
            elif token[1] == 'Number':
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
            if token[0] == 'sqrt':
                skipCounter = 1
                # TODO: Allow arithmetic / variable length arguments
                # TODO: Check for correct types
                newTokens.append('sqrt('+tokens[i+1]+')')
            if token[0] == 'remainder':
                skipCounter = 3
                # TODO: Allow arithmetic / variable length arguments
                # TODO: Check for correct types
                newTokens.append(tokens[i+1][0]+' % '+tokens[i+3][0])
        else:
            raise SyntaxError
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
    
