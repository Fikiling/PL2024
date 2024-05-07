import ply.yacc as yacc
from analex_forth import tokens
import analex_forth as analex 

myStack = []
functions = {}
codigo_forth = []
indice = -1
counter_IF = 1
flag_function = 0 # 0 -> não está dentro de uma função, 1 -> está dentro de uma função


# s : input FIM
# input : input linha
#       | empty
# linha : elem                                   
#       | 2PONTOS funcao input PONTOVIRGULA
#       | condicional
#       | ciclo
#       | variaveis
# funcao : FUNCAO
# elem : NUM                            DONE
#      | operador                       DONE
#      | ID                             DONE
#      | POINT                          DONE
#      | PRINTSTRING                    DONE
#      | SWAP                           DONE
#      | CR                             DONE
#      | EMIT                           DONE
#      | CHAR CARATER                   DONE
#      | SPACES                         DONE
#      | SPACE                          DONE       
#      | KEY                            DONE (half way)
#      | DUP                            DONE
#      | 2DUP                           DONE
#      | DROP                           DONE
#      | ROT
#      | OVER
#      | TUCK
#      | NIP
#      | NEG
#      | ABS
#      | MIN
#      | MAX
#      | AND
#      | OR
#      | XOR
#      | NOT
#      | LSHIFT
#      | RSHIFT
#      | BEGIN
#      | UNTIL
# operador : SOMA               
#          | SUBTRACAO
#          | DIVISAO
#          | MULTIPLICACAO
#          | RESTO
#          | POTENCIA
#          | DIVIDE_BY_2
#          | EQUAL
#          | SUP
#          | SUPEQUAL
#          | INF
#          | INFEQUAL
#          
# condicional : IF input ELSE input THEN input
#             | IF input THEN input
# empty :




def p_input(p):
    'input : input linha'
    p[0] = p[1] + p[2]

def p_input_empty(p):
    'input : empty'
    p[0] = ""

def p_linha_statement(p):
    'linha : elem'
    p[0] = p[1]

def p_linha_funcao(p):
    'linha : 2PONTOS funcao input PONTOVIRGULA'
    global functions, flag_function 
    flag_function = 0
    functions[p[2].strip()] = p[3]
    p[0] = ''
    

def p_linha_condicional(p):
    'linha : condicional'
    p[0] = p[1]


def p_funcao(p):
    'funcao : FUNCAO'
    global flag_function
    flag_function = 1
    p[0] = p[1] + '\n'
    
def p_elem_NUM(p):
    'elem : NUM'
    global myStack
    myStack.append(p[1])
    
    p[0] = '\tpushi ' + str(p[1]) + '\n'

def p_elem_operador(p):
    'elem : operador'
    p[0] = p[1]
    
def p_elem_POINT(p):
    'elem : POINT'
    global myStack, flag_function

    if flag_function == 0:
        if len(myStack) == 0:
            raise Exception('Not enough elements in the stack to perform an operation.')
        elem = myStack.pop()
    
        if type(elem) == int:
            p[0] = '\twrites\n'
        elif type(elem) == str:
            p[0] = '\twritei\n'
        else:
            raise Exception('Invalid type for operation, the last element in the stack must be an integer or a string.\n')
    else:
        p[0] = '\twritei\n'

def p_elem_PRINTSTRING(p):
    'elem : PRINTSTRING'
    p[0] = '\tpushs ' + p[1][1:] + '\n' + '\twrites \n'

def p_elem_SWAP(p):
    'elem : SWAP'
    global myStack, flag_function
    if flag_function == 0:
        if len(myStack) < 2:
            raise Exception('Not enough elements in the stack to perform an operation.')
        elem1 = myStack.pop()
        elem2 = myStack.pop()
        myStack.append(elem1)
        myStack.append(elem2)
        p[0] = '\tswap\n'
    else:
        p[0] = '\tswap\n'

def p_elem_CR(p):
    'elem : CR'
    p[0] = '\twriteln \n'

#--------------------------------------------------------
def p_elem_EMIT(p):
    'elem : EMIT'
    global myStack, flag_function
    if flag_function == 0:
        if len(myStack) == 0:
            raise Exception('Not enough elements in the stack to perform an operation.')
        elem = myStack.pop()
        if type(elem) != int:
            raise Exception('Invalid type for operation, the last element in the stack must be an integer.\n')
        else:
            p[0] = '\writechr\n'
    else:
        p[0] = '\writechr\n'

def p_elem_CHAR(p):
    'elem : CHAR CARATER'
    global myStack
    myStack.append(ord(p[2]))
    p[0] = '\tpushi ' + str(ord(p[2])) + '\n'

def p_elem_SPACES(p):
    'elem : SPACES'
    global myStack
    if len(myStack):
        raise Exception('Not enough elements in the stack to perform an operation.')
    elem = myStack.pop()
    if type(elem) != int:
        raise Exception('Invalid type for operation, the last element in the stack must be an integer.\n')
    result = '\tSPACES:\n'
    for i in range(elem):
        result += '\t\tpushs " "\n'
        result += '\t\twrites\n'
    p[0] = result

def p_elem_SPACE(p):
    'elem : SPACE'
    p[0] = '\tpushs " "\n' + '\twrites\n' 

def p_elem_KEY(p):
    'elem : KEY'
    p[0] = '\tread\n \tchrcode\n'

def p_elem_DUP(p):
    'elem : DUP'
    global myStack, flag_function

    if flag_function == 0:
        if len(myStack) == 0:
            raise Exception('Not enough elements in the stack to perform an operation.')
        elem = myStack.pop()
        myStack.append(elem)
        myStack.append(elem)
        p[0] = '\tdup 1\n'
    else:
        p[0] = '\tdup 1\n'

def p_elem_2DUP(p):
    'elem : 2DUP'
    global myStack
    
    if len(myStack) < 2:
        raise Exception('Not enough elements in the stack to perform an operation.')
    
    elem1 = myStack.pop()
    elem2 = myStack.pop()
    code = '\tpop 2\n'
    if (type(elem1) == int and type(elem2) != int):
        code += f'\tpushi {elem1}\n\tpushs {elem2}\n\tpushi {elem1}\n\tpushs {elem2}\n'
    if (type(elem1) == int and type(elem2) == int):
        code += f'\tpushi {elem1}\n\tpushi {elem2}\n\tpushi {elem1}\n\tpushi {elem2}\n'
    elif (type(elem1) != int and type(elem2) == int):
        code += f'\tpushs {elem1}\n\tpushi {elem2}\n\tpushs {elem1}\n\tpushi {elem2}\n'
    else:
        code += f'\tpushs {elem1}\n\tpushs {elem2}\n\tpushs {elem1}\n\tpushs {elem2}\n'

    myStack.append(elem2)
    myStack.append(elem1)
    myStack.append(elem2)
    myStack.append(elem1)
    
    p[0] = code

def p_elem_DROP(p):
    'elem : DROP'
    global myStack, flag_function

    if flag_function == 0:
       if len(myStack) > 0: 
            myStack.pop()
       p[0] = '\tpop 1\n'
    else:
        p[0] = '\tpop 1\n'

def p_elem_ID(p):
    'elem : ID'
    global functions
    if p[1] not in functions:
        raise Exception(f'Function {p[1]} is not defined.')

    # Adiciona indentação extra se a função for chamada dentro de outra função
    if '\t' in functions[p[1]]:
        indented_function = functions[p[1]].replace('\n', '\n\t')
    else:
        indented_function = functions[p[1]]

    # Adiciona a tabulação correspondente à profundidade do aninhamento
    depth = p.slice[1].lineno - 1
    indent = '\t' * depth
    p[0] = indent + p[1] + ':\n' + indent + '\t' + indented_function + '\n'

def p_operador(p):
    '''operador : SOMA
                | SUBTRACAO
                | DIVISAO
                | MULTIPLICACAO
                | RESTO
                | POTENCIA
                | DIVIDE_BY_2
                | EQUAL
                | SUP
                | SUPEQUAL
                | INF
                | INFEQUAL
    '''
    global myStack, flag_function

    if flag_function == 0:
        if (len(myStack) < 2):
            raise Exception('Not enough elements in the stack to perform an operation.')
        
        elem1 = myStack.pop()      # ultimo 
        elem2 = myStack.pop()      # primeiro  
        
        if (type(elem1) == int and type(elem2) == int):

            if p[1] == '+':
                myStack.append(elem2 + elem1)
                p[0] = '\tadd\n'
            elif p[1] == '-':
                myStack.append(elem2 - elem1)
                p[0] = '\tsub\n'
            elif p[1] == '/':
                myStack.append(elem2 / elem1)
                p[0] = '\tdiv\n'
            elif p[1] == '*':
                myStack.append(elem2 * elem1)
                p[0] = '\tmul\n'
            elif p[1] == '%':
                myStack.append(elem2 % elem1)
                p[0] = '\tmod\n'
            elif p[1] == '^':
                myStack.append(elem2 ** elem1)
                p[0] = '\tpow\n'
            elif p[1] == '/2':
                myStack.append(elem2)
                myStack.append(elem1 / 2)
                p[0] = '\tpushi 2\n'+ '\tdiv\n'
            elif p[1] == '=':
                if elem2 == elem1:
                    myStack.append(1)
                else:
                    myStack.append(0)
                p[0] = '\tequal\n'
            elif p[1] == '>':
                if elem2 > elem1:
                    myStack.append(1)
                else:
                    myStack.append(0)       
                p[0] = '\tsup\n'
            elif p[1] == '>=':
                if elem2 >= elem1:
                    myStack.append(1)
                else:
                    myStack.append(0)
                p[0] = '\tsupeq\n'
            elif p[1] == '<':
                if elem2 < elem1:
                    myStack.append(1)
                else:
                    myStack.append(0)
                p[0] = '\tinf\n'
            elif p[1] == '<=':
                if elem2 <= elem1:
                    myStack.append(1)
                else:
                    myStack.append(0)
                p[0] = '\tinfeq\n'
        else:
            raise Exception('Invalid types for operation, the last two elements in the stack must be integers.\n')
    else:
        if p[1] == '+':
            p[0] = '\tadd\n'
        elif p[1] == '-':
            p[0] = '\tsub\n'
        elif p[1] == '/':
            p[0] = '\tdiv\n'
        elif p[1] == '*':
            p[0] = '\tmul\n'
        elif p[1] == '%':
            p[0] = '\tmod\n'
        elif p[1] == '^':
            p[0] = '\tpow\n'
        elif p[1] == '/2':
            p[0] = '\tpushi 2\n'+ '\tdiv\n'
        elif p[1] == '=':
            p[0] = '\tequal\n'
        elif p[1] == '>':
            p[0] = '\tsup\n'
        elif p[1] == '>=':
            p[0] = '\tsupeq\n'
        elif p[1] == '<':
            p[0] = '\tinf\n'
        elif p[1] == '<=':
            p[0] = '\tinfeq\n'



def p_cond_else(p):
    'condicional : IF input ELSE input THEN input'
    global counter_IF
    p[0] = '\tjz else' + str(counter_IF) +'\n' + p[2] + 'jump endif' + str(counter_IF) + '\n' + 'else' + str(counter_IF) + ':\n' + p[4] + 'endif' + str(counter_IF) + ':\n' + p[6]
    counter_IF += 1
    

def p_cond_then(p):   
    'condicional : IF input THEN input'
    global counter_IF
    p[0] = '\tjz endif' + str(counter_IF) +'\n' + p[2] + 'jump endif' + str(counter_IF) + '\n' + 'endif' + str(counter_IF) + ':\n' + p[4]
    counter_IF += 1


def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print("Erro de sintaxe em", p)
    else:
        print("Erro de sintaxe no final do input")



# -----------------------Rodar o Programa----------------------------

parser = yacc.yacc()

analex.lex.flagFunction = 0
with open("input.txt", "r") as file:
    codigo = file.read()

result = parser.parse(codigo)

with open("output.txt", "w") as file:
    file.write("START\n\n")
    file.write(result)
    file.write("\nSTOP")



# -----------------------Minhas Funções----------------------------


def input_multiline():
    global codigo_forth
    global indice
    linha = ""
    
    while linha != "FIM":
        linha = input()
        if linha != "FIM":
            codigo_forth.append(linha)
            indice += 1
    print("------------------FIM DE BLOCO-----------------")



'''
print("Regras de escrita:")
print("     FIM -> fim de bloco de código")
print("     CTRL+D > termina o programa.")
print("Digite seu código FORTH:")

try:
        while True:
            # Receber input
            input_multiline()
            codigo_forth_completo = '\n'.join(codigo_forth)
            
            # Processar input
            analex.lex.flagFunction = 0
            result = parser.parse(codigo_forth_completo)
            print(result)

except EOFError:  # Captura Ctrl+D 
        print("Ctrl+D recebido ---> Programa a encerrar.")
'''

