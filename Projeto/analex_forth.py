import ply.lex as lex

# Lista de tokens soma, adição, subtração, divisão, resto da divisão inteira, potência
tokens = [
    'NUM',
    'SOMA',
    'SUBTRACAO',
    'DIVISAO',
    'MULTIPLICACAO',
    'RESTO',
    'POTENCIA'
]

def t_NUM(t):
    r'\d+'
    lex.num += 1
    t.value = int(t.value)
    return t

def t_SOMA(t):
    r'\+'
    lex.num -= 1
    if lex.num < 1: 
        raise SyntaxError("Número de operadores maior ou igual que o número de operandos")
    return t

def t_SUBTRACAO(t):
    r'\-'
    lex.num -= 1
    if lex.num < 1: 
        raise SyntaxError("Número de operadores maior ou igual que o número de operandos")
    return t

def t_DIVISAO(t):
    r'\/'
    lex.num -= 1
    if lex.num < 1: 
        raise SyntaxError("Número de operadores maior ou igual que o número de operandos")
    return t

def t_MULTIPLICACAO(t):
    r'\*'
    lex.num -= 1
    if lex.num < 1: 
        raise SyntaxError("Número de operadores maior ou igual que o número de operandos")
    return t

def t_RESTO(t):
    r'\%'
    lex.num -= 1
    if lex.num < 1: 
        raise SyntaxError("Número de operadores maior ou igual que o número de operandos")
    return t

def t_POTENCIA(t):
    r'\^'
    lex.num -= 1
    if lex.num < 1: 
        raise SyntaxError("Número de operadores maior ou igual que o número de operandos")
    return t

t_ignore = ' \n\t'

def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)

lex = lex.lex()
lex.num = 0
