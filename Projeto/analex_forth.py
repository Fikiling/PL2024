import ply.lex as lex


# Lista de tokens 
tokens = (
    'NUM',
    'SOMA',
    'SUBTRACAO',
    'DIVISAO',
    'MULTIPLICACAO',
    'RESTO',
    'POTENCIA',
    '2PONTOS',
    'PONTOVIRGULA',
    'EQUAL',
    'POINT',
    'PRINTSTRING',
    'DIVIDE_BY_2',
    'SWAP',
    'CR',
    'EMIT',
    'SPACES',
    'SPACE',
    'KEY',
    'DUP',
    '2DUP',
    'DROP',
    'SUP',
    'SUPEQUAL',
    'INF',
    'INFEQUAL',
    'IF',
    'ELSE',
    'THEN',
    'DO',
    'LOOP',
    'I_COUNTER',
    'CHAR',
    'VAR_DECLARACAO',
    'VAR_ATRIBUICAO',
    'VAR_CHAMADA',
    'FUNCAO',
    'ID'
)

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

def t_PONTOVIRGULA(t):
    r'(?<!\S)\;(?!\S)'
    lex.flagFunction = 0
    t.value = 'PONTOVIRGULA'
    return t

def t_EQUAL(t):
    r'(?<!\S)\=(?!\S)'
    return t

def t_POINT(t):
    r'(?<!\S)\.(?!\S)'
    return t

def t_PRINTSTRING(t):
    r'(?<!\S)\."[^"]*"(?!\S)|(?<!\S)\.\([^"]*\)(?!\S)'
    return t

def t_DIVIDE_BY_2(t):
    r'(?<!\S)2\/(?!\S)'
    return t

def t_SWAP(t):
    r'(?i)(?<!\S)swap(?!\S)'
    return t

def t_CR(t):
    r'(?i)(?<!\S)cr(?!\S)'
    return t

def t_EMIT(t):
    r'(?i)(?<!\S)emit(?!\S)'
    return t

def t_SPACES(t):
    r'(?i)(?<!\S)spaces(?!\S)'
    return t

def t_SPACE(t):
    r'(?i)(?<!\S)space(?!\S)'
    return t

def t_KEY(t):
    r'(?i)(?<!\S)key(?!\S)'
    return t

def t_DUP(t):
    r'(?i)(?<!\S)dup(?!\S)'
    return t

def t_2DUP(t):
    r'(?i)(?<!\S)2dup(?!\S)'
    return t

def t_DROP(t):
    r'(?i)(?<!\S)drop(?!\S)'
    return t

def t_SUP(t):
    r'(?i)(?<!\S)\>(?!\S)'
    return t

def t_SUPEQUAL(t):
    r'(?i)(?<!\S)\>=(?!\S)'
    return t

def t_INF(t):
    r'(?i)(?<!\S)\<(?!\S)'
    return t

def t_INFEQUAL(t):
    r'(?i)(?<!\S)\<=(?!\S)'
    return t

def t_IF(t):
    r'(?i)(?<!\S)if(?!\S)'
    return t

def t_ELSE(t):
    r'(?i)(?<!\S)else(?!\S)'
    return t

def t_THEN(t):
    r'(?i)(?<!\S)then(?!\S)'
    return t

def t_DO(t):
    r'(?i)(?<!\S)do(?!\S)'
    return t

def t_LOOP(t):
    r'(?i)(?<!\S)loop(?!\S)'
    return t

def t_I_COUNTER(t):
    r'(?i)(?<!\S)i(?!\S)'
    return t

def t_CHAR(t):
    r'(?i)(?<!\S)char\s.(?!\S)'
    return t

def t_VAR_DECLARACAO(t):
    r'(?i)(?<!\S)variable\s[A-Za-z0-9_]+(?!\S)'
    return t

def t_VAR_ATRIBUICAO(t):
    r'(?i)(?<!\S)[A-Za-z0-9_]+\s+!(?!\S)'
    return t

def t_VAR_CHAMADA(t):
    r'(?i)(?<!\S)[A-Za-z0-9_]+\s@(?!\S)'
    return t

def t_beginF_FUNCAO(t):
    r'(?<!\S)[a-zA-Z_-][a-zA-Z_123456789-]*(?!\S)'

    if lex.flagFunction == 1: 
        raise SyntaxError("Não é possível definir uma função dentro de outra função")

    lex.flagFunction = 1
    t.lexer.functions.append(t.value)
    t.lexer.begin('INITIAL')
    return t

def t_ID(t):
    r'(?<!\S)[a-zA-Z_][a-zA-Z_0-9!?\-]*(?!\S)'
    if t.type == 'ID':
        if (t.value in t.lexer.functions):
            return t
        else:
            raise Exception(f'Function {t.value} is not defined.')
        
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
CHAR W .
CHAR % DUP . EMIT
CHAR A DUP .
32 + EMIT
"""

lex.input(file)

while tok := lex.token():
    print(tok)

'''