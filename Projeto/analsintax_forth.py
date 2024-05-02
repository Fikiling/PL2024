import ply.yacc as yacc
from analex_forth import tokens
import analex_forth as analex 

functions = {}
codigo_forth = []
indice = -1

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
#      | POINTSTRING    
#      | CR
#      | EMIT
#      | CHAR
#      | DROP
#      | SWAP
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
#      | SPACES
#      | SPACE
#      | DUP
#      | KEY
# operador : SOMA               
#          | SUBTRACAO
#          | DIVISAO
#          | MULTIPLICACAO
#          | RESTO
#          | POTENCIA
#          | DIVIDE_BY_2
#
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
    global functions
    functions[p[2].strip()] = p[3]
    p[0] = ''

def p_funcao(p):
    'funcao : FUNCAO'
    p[0] = p[1] + '\n'
    
def p_elem_NUM(p):
    'elem : NUM'
    p[0] = 'pushi ' + str(p[1]) + '\n'

def p_elem_operador(p):
    'elem : operador'
    p[0] = p[1]

def p_elem_ID(p):
    'elem : ID'
    global functions
    if p[1] not in functions:
        raise Exception(f'Function |{p[1]}| is not defined.')
    p[0] = 'pusha ' + p[1] + '\n' + 'call\n'

def p_elem_POINT(p):
    'elem : POINT'
    p[0] = 'writei \n'

def p_operador_SOMA(p):
    'operador : SOMA'
    p[0] = 'add\n'

def p_operador_SUBTRACAO(p):
    'operador : SUBTRACAO'
    p[0] = 'sub\n'

def p_operador_DIVISAO(p):
    'operador : DIVISAO'
    p[0] = 'div\n'

def p_operador_MULTIPLICACAO(p):
    'operador : MULTIPLICACAO'
    p[0] = 'mul\n'

def p_operador_RESTO(p):
    'operador : RESTO'
    p[0] = 'mod\n'

def p_operador_POTENCIA(p):
    'operador : POTENCIA'
    p[0] = 'pow\n'

def p_operador_DIVIDE_BY_2(p):
    'operador : DIVIDE_BY_2'
    p[0] = 'pushi 2\n'+ 'div\n'

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print("Erro de sintaxe em", p)
    else:
        print("Erro de sintaxe no final do input")


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

# -----------------------Rodar o Programa----------------------------

parser = yacc.yacc()

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

analex.lex.flagFunction = 0
with open("data.txt", "r") as file:
    codigo = file.read()


result = parser.parse(codigo)

with open("output.txt", "w") as file:
    file.write(result)
    
    file.write("\n")
    for elem in functions:
        file.write(elem + ":\n")
        formatted_string = "\t" + functions[elem].replace("\n", "\n\t") + "return"
        file.write(formatted_string)