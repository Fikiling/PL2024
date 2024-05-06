from testeLex import tokens
import ply.yacc as yacc

stack = []
functions = {}
functionBodyFlag = False
ifCounter = 0
ifIDStack = []
elseCounter = 0

#expressionList : exp expressionList
#                 | ε
#
#exp : operandList operation 
#    | DPOINTS function expressionList ENDFUNCTION
#
#operandList : operand operandList 
#            | CHAR CHARACTER 
#            | ε
#
#function : FUNCTION
#
#operand : NUM
#
#operation : +   
#          | * 
#          | / 
#          | % 
#          | - 
#          | PRINT
#          | DUP 
#          | EMIT 
#          | KEY 
#          | CR 
#          | SPACE 
#          | SPACES 
#          | PRINTTEXT 
#          | SWAP 
#          | 2DUP 
#          | COMPARISION 
#          | IF expressionList else THEN 
#          | FUNCTIONCALL 
#          | ε
#
#else : ELSE expressionList 
#    | ε


def p_expressionList_exp(p):
    'expressionList : exp expressionList'
    p[0] = '' + p[1] + p[2]

def p_expressionList_empty(p):
    'expressionList : empty'
    p[0] = ''

def p_exp_operandList(p):
    'exp : operandList operation'
    p[0] = p[1] + p[2]

def p_exp_DPOINTS(p):
    'exp : DPOINTS function expressionList ENDFUNCTION'
    global functionBodyFlag
    functions[p[2]] = p[3]
    functionBodyFlag = False
    p[0] = ''

def p_function(p):
    'function : FUNCTION'
    global functionBodyFlag
    if (functionBodyFlag):
        raise Exception('Cant define a function inside another function.')
    functionBodyFlag = True
    p[0] = p[1]


def p_operandList_operand(p):
    'operandList : operand operandList'
    p[0] = p[1] + p[2]

def p_operandList_CHAR(p):
    'operandList : CHAR CHARACTER'
    stack.append(ord(p[2]))
    p[0] = 'pushi ' + str(ord(p[2])) + '\n'

def p_operandList_empty(p):
    'operandList : empty'
    p[0] = ''

def p_operand_NUM(p):
    'operand : NUM'
    p[0] = 'pushi ' + str(p[1]) + '\n'
    stack.append(p[1])

def p_operation(p):
    '''operation : '+'
                 | '-'
                 | '*'
                 | '/'
                 | '%'
                 | PRINT
                 | DUP
                 | EMIT
                 | KEY
                 | CR
                 | SPACE
                 | SPACES
                 | SWAP
                 | 2DUP
    '''
    global functionBodyFlag
    if (not functionBodyFlag):
        if ((len(stack)<1 and p[1] in ['PRINT', 'DUP', 'EMIT', 'SPACES']) or (len(stack)<2 and p[1] in ['+', '-', '*', '/', '%', 'SWAP', '2DUP'])):
            if (len(stack)==0):
                stack_content = '|  |'
            else:
                stack_content = '| ' + str(stack.pop()) + ' |\n'
                for item in stack:
                    stack_content += '       | ' + str(item) + ' |\n'

            raise Exception(f'Not enough operands in the stack to perform the operation "{p[1]}".\n\n Stack:{stack_content}')
        elif p[1] == 'SPACES':
            string = 'pop 1\npushs "'

            n_spaces = stack.pop()
            if type(n_spaces) == int:
                for i in range(n_spaces):
                    string += ' '
                string += '"\nwrites\n'
                p[0] = string
            else:
                if (len(stack)==0):
                    stack_content = '|  |'
                else:
                    stack_content = '| ' + str(stack.pop()) + ' |\n'
                    for item in stack:
                        stack_content += '       | ' + str(item) + ' |\n'
                
                raise Exception(f'No integer on top of the stack to perform the operation "{p[1]}".\n\n Stack:{stack_content}')
        elif p[1] == 'SPACE':
            p[0] = 'pushs " "\nwrites\n'
        elif p[1] == 'CR':
            p[0] = 'writeln\n'
        elif p[1] == 'KEY':

            # Falta Adicionar código para assegurar que é só um caracter e não vários

            stack.append('X')
            p[0] = 'read\n'
        elif p[1] == '.':
            value = stack.pop()
            print(f'PRINT -> {value}')
            if type(value) == int:
                p[0] = 'writei\n'
            else:
                p[0] = 'writes\n'
        elif p[1] == 'DUP':
            value = stack.pop()
            stack.append(value)
            stack.append(value)
            p[0] = 'dup 1\n'
        elif p[1] == 'EMIT':
            value = stack.pop()
            if type(value) == int:
                print(f'EMIT -> {chr(value)}')
                p[0] = 'pop 1\npushs "' + chr(value) + '"\nwrites\n'
            else:
                if (len(stack)==0):
                    stack_content = '|  |'
                else:
                    stack_content = '| ' + str(stack.pop()) + ' |\n'
                    for item in stack:
                        stack_content += '       | ' + str(item) + ' |\n'
                
                raise Exception(f'No integer on top of the stack to perform the operation "{p[1]}".\n\n Stack:{stack_content}')
        elif p[1] == 'SWAP':
            value1 = stack.pop()
            value2 = stack.pop()
            string = 'pop 2\n'
            stack.append(value1)
            stack.append(value2)
            p[0] = 'swap\n'
        elif p[1] == '2DUP':
            value1 = stack.pop()
            value2 = stack.pop()
            string = 'pop 2\n'
            if (type(value1) == int and type(value2) == int):
                string += f'pushi {value1}\npushi {value2}\npushi {value1}\npushi {value2}\n'
            elif (type(value1) != int and type(value2) == int):
                string += f'pushs {value1}\npushi {value2}\npushs {value1}\npushi {value2}\n'
            elif (type(value1) == int and type(value2) != int):
                string += f'pushi {value1}\npushs {value2}\npushi {value1}\npushs {value2}\n'
            else:
                string += f'pushs {value1}\npushs {value2}\npushs {value1}\npushs {value2}\n'
            stack.append(value2)
            stack.append(value1)
            stack.append(value2)
            stack.append(value1)
            p[0] = string
        elif p[1] in ['+', '-', '*', '/', '%']:
            num1 = stack.pop()
            num2 = stack.pop()
            if type(num1) == int and type(num2) == int:
                if p[1] == '+':
                    stack.append(num1 + num2)
                    p[0] = 'add\n'
                elif p[1] == '-':
                    stack.append(num1 - num2)
                    p[0] = 'sub\n'
                elif p[1] == '*':
                    stack.append(num1 * num2)
                    p[0] = 'mul\n'
                elif p[1] == '/':
                    stack.append(num1 / num2)
                    p[0] = 'div\n'
                elif p[1] == '%':
                    stack.append(num1 % num2)
                    p[0] = 'mod\n'
            else:
                if (len(stack)==0):
                    stack_content = '|  |'
                else:
                    stack_content = '| ' + str(stack.pop()) + ' |\n'
                    for item in stack:
                        stack_content += '       | ' + str(item) + ' |\n'
                
                raise Exception(f'No tow integers on top of the stack to perform the operation "{p[1]}".\n\n Stack:{stack_content}')
    else:
        if p[1] == 'SPACES':
            p[0] = 'WHILE0:\npushi 1\nsub\npushs " "\nwrites\ndup 1\njz ENDWHILE0\njump WHILE0\nENDWHILE0:'             
        elif p[1] == 'SPACE':
            p[0] = 'pushs " "\nwrites\n'
        elif p[1] == 'CR':
            p[0] = 'writeln\n'
        elif p[1] == 'KEY':

            # Falta Adicionar código para assegurar que é só um caracter e não vários

            p[0] = 'read\n'
        elif p[1] == '.':
            p[0] = 'writei\n'
        elif p[1] == 'DUP':
            p[0] = 'dup 1\n'
        elif p[1] == 'EMIT':

            # CORRIGIR

            p[0] = 'ERROR\n'
        elif p[1] == 'SWAP':
            p[0] = 'swap\n'
        elif p[1] == '2DUP':

            # CORRIGIR

            p[0] = 'ERROR\n'
        elif p[1] in ['+', '-', '*', '/', '%']:
            if p[1] == '+':
                p[0] = 'add\n'
            elif p[1] == '-':
                p[0] = 'sub\n'
            elif p[1] == '*':
                p[0] = 'mul\n'
            elif p[1] == '/':
                p[0] = 'div\n'
            elif p[1] == '%':
                p[0] = 'mod\n'

def p_operation_PRINTTEXT(p):
    'operation : PRINTTEXT'
    p[0] = 'pushs "' + p[1] + '"\nwrites\n'

def p_operation_COMPARISION(p):
    'operation : COMPARISION'
    global functionBodyFlag
    if (not functionBodyFlag):
        if ((len(stack)<1 and p[1] in ['0=', '0<', '0>']) or (len(stack)<2 and p[1] in ['=', '<>', '<', '>'])):
            if (len(stack)==0):
                stack_content = '|  |'
            else:
                stack_content = '| ' + str(stack.pop()) + ' |\n'
                for item in stack:
                    stack_content += '       | ' + str(item) + ' |\n'

            raise Exception(f'Not enough operands in the stack to perform the operation "{p[1]}".\n\n Stack:{stack_content}')

    if p[1] == '0=':
        p[0] = 'pushi 0\nequal\n'
    elif p[1] == '0<':
        p[0] = 'pushi 0\ninf\n'
    elif p[1] == '0>':
        p[0] = 'pushi 0\nsup'
    elif p[1] in ['=', '<>', '<', '>']:
        if (not functionBodyFlag):
            stack.pop()
        if p[1] == '=':
            p[0] = 'equal\n'
        elif p[1] == '<>':
            p[0] = 'sub\npushi 0\nequal\npushi 0\nequal\n'
        elif p[1] == '<':
            p[0] = 'inf\n'
        elif p[1] == '>':
            p[0] = 'sup\n'

def p_operation_IF(p):
    'operation : IF expressionList else THEN'
    global functionBodyFlag
    if (not functionBodyFlag):
        if (len(stack)<1):
            stack_content = '|  |'
            raise Exception(f'Not enough operands in the stack to perform the operation "{p[1]}".\n\n Stack:{stack_content}')
        stack.pop()
    
    global ifIDStack
    ifId = ifIDStack.pop()
    
    p[0] = 'jz ELSE' + str(ifId) + '\n' + p[2] + p[3]

def p_else_ELSE(p):
    'else : ELSE expressionList'
    global ifCounter
    global ifIDStack
    ifId = ifCounter
    ifIDStack.append(ifId)
    ifCounter += 1


    global elseCounter
    elseId = elseCounter
    elseCounter += 1
    
    p[0] = 'jump ENDIF' + str(elseId) + '\n' + 'ELSE' + str(ifId) + ':\n' + p[2] + 'ENDIF' + str(elseId) + ':\n'

def p_else_empty(p):
    'else : empty'
    global ifCounter
    global ifIDStack
    ifId = ifCounter
    ifIDStack.append(ifId)
    ifCounter += 1
    
    p[0] = 'ELSE' + str(ifId) + ':\n'

def p_operation_FUNCTIONCALL(p):
    'operation : FUNCTIONCALL'
    global functionBodyFlag
    if p[1] not in functions:
        raise Exception(f'Function {p[1]} is not defined.')
    
    p[0] = functions[p[1]]

def p_operation_empty(p):
    'operation : empty'
    p[0] = ''

def p_empty(p):
    'empty : '
    pass

def p_error(p):
    print("Erro sintático no input!")
    print(p)

file = """
: AVERAGE ( a b -- avg ) + 2/ ;
10 20 AVERAGE .

"""

parser = yacc.yacc()
with open("output.txt", "w") as output_file:
    output_file.write(parser.parse(file))

'''
expressionList : exp expressionList
               | ε

exp : operandList operation
    | DPOINTS function expressionList ENDFUNCTION

operandList : operand operandList
            | CHAR CHARACTER
            | ε

function : FUNCTION

operand : NUM

operation : +
          | *
          | /
          | %
          | -
          | PRINT
          | DUP
          | EMIT
          | KEY
          | CR
          | SPACE
          | SPACES
          | PRINTTEXT
          | SWAP
          | 2DUP
          | COMPARISION
          | IF expressionList else THEN
          | FUNCTIONCALL
          | ε

else : ELSE expressionList
     | ε
'''