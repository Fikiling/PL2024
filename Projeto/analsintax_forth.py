import ply.yacc as yacc
from analex_forth import tokens
import analex_forth as analex 

# input : input linha
#       | empty
# linha : expNum
#       | função
#       | print
#       | condicional
#       | ciclo
#       | variaveis
# expNum : expNum fator
#        | fator
# fator : NUM
#       | operador 



def p_input(p):
    'input : input linha'
    p[0] = p[1] + p[2]

def p_input_empty(p):
    'input : empty'
    p[0] = ''

def p_linha_expNum(p):
    'linha : expNum'
    p[0] = p[1]
    
def p_expNum_composta(p):
    'expNum : expNum fator'
    p[0] = p[1] + p[2] 

def p_expNum_simples(p):
    'expNum : fator'
    p[0] = p[1] 

def p_fator_NUM(p):
    'fator : NUM'
    p[0] = 'pushi ' + str(p[1]) + '\n'

def p_fator_operador(p):
    'fator : operador'
    p[0] = p[1]


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

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print("Erro de sintaxe em", p)
    else:
        print("Erro de sintaxe no final do input")

parser = yacc.yacc()

while s := input('Digite código FORTH > '):
    print("\nstart\n")
    analex.lex.num = 0
    result = parser.parse(s)
    print(result)
    print("stop\n")