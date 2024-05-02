import ply.lex as lex

#NOTA: Formula para forçar TXT a estar separado de outros tokens: (?<!\S)TXT(?!\S)

# Palavras reservadas Forth
reserved = {
    'dup': 'DUP',
    'drop': 'DROP',
    'swap': 'SWAP',
    'rot': 'ROT',
    'over': 'OVER',
    'tuck': 'TUCK',
    'nip': 'NIP',
    'neg': 'NEG',
    'abs': 'ABS',
    'min': 'MIN',
    'max': 'MAX',
    'and': 'AND',
    'or': 'OR',
    'xor': 'XOR',
    'not': 'NOT',
    'lshift': 'LSHIFT',
    'rshift': 'RSHIFT',
    'begin': 'BEGIN',
    'until': 'UNTIL',
    'emit': 'EMIT',
    'cr': 'CR',
    'spaces': 'SPACES',
    'space': 'SPACE',
    'char': 'CHAR',
    'key': 'KEY',
    'if': 'IF',
    'else': 'ELSE',
    'then': 'THEN',
    'while': 'WHILE',
    'repeat': 'REPEAT',
    'do': 'DO',
    'loop': 'LOOP',
    'variable': 'VARIABLE',

}

# Lista de tokens soma, adição, subtração, divisão, resto da divisão inteira, potência
tokens = (
    'NUM',
    'SOMA',
    'SUBTRACAO',
    'DIVISAO',
    'MULTIPLICACAO',
    'RESTO',
    'POTENCIA',
    '2PONTOS',
    'FUNCAO',
    'PONTOVIRGULA',
    'ID',
    'ZEROEQUAL',
    'ZEROLESS',
    'ZEROGREAT',
    'EQUAL',
    'LESS',
    'GREAT',
    'POINT',
    'POINTSTRING',
    'DIVIDE_BY_2',
) + tuple(reserved.values())

states = (
    ('beginF', 'exclusive'), 
)

def t_commentary(t):
    r'\( .* \)'
    pass

def t_NUM(t):
    r'(?<!\S)\d+(?!\S)'
    t.value = int(t.value)
    return t

def t_SOMA(t):
    r'(?<!\S)\+(?!\S)'
    t.value = 'SOMA'
    return t

def t_SUBTRACAO(t):
    r'(?<!\S)\-(?!\S)'
    t.value = 'SUBTRACAO'
    return t

def t_DIVISAO(t):
    r'(?<!\S)\/(?!\S)'
    t.value = 'DIVISAO'
    return t

def t_MULTIPLICACAO(t):
    r'(?<!\S)\*(?!\S)'
    t.value = 'MULTIPLICACAO'
    return t

def t_RESTO(t):
    r'(?<!\S)\%(?!\S)'
    t.value = 'RESTO'
    return t

def t_POTENCIA(t):
    r'(?<!\S)\^(?!\S)'
    t.value = 'POTENCIA'
    return t

def t_2PONTOS(t):
    r'(?<!\S)\:(?!\S)'
    t.value = '2PONTOS'
    t.lexer.begin('beginF')
    return t

def t_beginF_FUNCAO(t):
    r'(?<!\S)[a-zA-Z_][a-zA-Z_123456789]*(?!\S)'

    if lex.flagFunction == 1: 
        raise SyntaxError("Não é possível definir uma função dentro de outra função")

    lex.flagFunction = 1
    t.lexer.functions.append(t.value)
    t.lexer.begin('INITIAL')
    return t

def t_PONTOVIRGULA(t):
    r'(?<!\S)\;(?!\S)'
    lex.flagFunction = 0
    t.value = 'PONTOVIRGULA'
    return t

def t_ID(t):
    r'(?<!\S)[a-zA-Z_][a-zA-Z_0-9]*(?!\S)'
    if t.type == 'ID':
        if (t.value in t.lexer.functions):
            return t
        elif (t.value not in reserved):
            raise Exception(f'Function {t.value} is not defined.')
        
    return t

def t_ZEROEQUAL(t):
    r'(?<!\S)\=0(?!\S)'
    return t

def t_ZEROLESS(t):
    r'(?<!\S)\<0(?!\S)'
    return t

def t_ZEROGREAT(t):
    r'(?<!\S)\>0(?!\S)'
    return t

def t_EQUAL(t):
    r'(?<!\S)\=(?!\S)'
    return t

def t_LESS(t):
    r'(?<!\S)\<(?!\S)'
    return t

def t_GREAT(t):
    r'(?<!\S)\>(?!\S)'
    return t

def t_POINT(t):
    r'(?<!\S)\.(?!\S)'
    return t

def t_POINTSTRING(t):
    r'(?<!\S)\s\.\"(.*)+\"(?!\S)'
    return t

def t_DIVIDE_BY_2(t):
    r'(?<!\S)2\/(?!\S)'
    return t

t_ignore = ' \n\t'
t_beginF_ignore = ' \n\t'

def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)

def t_beginF_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)

lex = lex.lex()
lex.begin('INITIAL')

lex.functions = []
lex.flagFunction = 0

'''

file = """
: AVERAGE  + 2/ ;
10 20 AVERAGE .
do
"""

lex.input(file)

while tok := lex.token():
    print(tok)

'''