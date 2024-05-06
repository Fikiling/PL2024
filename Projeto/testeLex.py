import ply.lex as lex
import re

tokens = (
    'NUM',
    'PRINT',
    'CHAR',
    'CHARACTER',
    'DUP',
    'EMIT',
    'KEY',
    'CR',
    'SPACE',
    'SPACES',
    'PRINTTEXT',
    'SWAP',
    '2DUP',
    'DPOINTS',
    'FUNCTION',
    'ENDFUNCTION',
    'FUNCTIONCALL',
    'COMPARISION',
    'IF',
    'ELSE',
    'THEN'
)

states = (
    ('charON', 'exclusive'),
    ('funtionOn', 'exclusive')
)

literals = ['+', '-', '*', '/', '%']

def t_comment(t):
    r'\( .* \)'
    pass

def t_funtionOn_FUNCTION(t):
    r'[a-zA-Z_][a-zA-Z_123456789]+'
    t.lexer.functions.append(t.value)
    t.lexer.begin('INITIAL')
    return t

def t_IF(t):
    r'IF'
    t.value = 'IF'
    return t

def t_ELSE(t):
    r'ELSE'
    t.value = 'ELSE'
    return t

def t_THEN(t):
    r'THEN'
    t.value = 'THEN'
    return t

def t_DPOINTS(t):
    r':'
    t.value = 'DPOINTS'
    t.lexer.begin('funtionOn')
    return t

def t_COMPARISION(t):
    r'(=|<>|<|>|0=|0<|0>)'
    return t

def t_charON_CHARACTER(t):
    r'.'
    t.lexer.begin('INITIAL')
    return t

def t_CHAR(t):
    r'CHAR'
    t.lexer.begin('charON')
    return t

def t_ENDFUNCTION(t):
    r';'
    t.value = 'ENDFUNCTION'
    return t

def t_2DUP(t):
    r'2dup'
    t.value = '2DUP'
    return t

def t_SWAP(t):
    r'swap'
    t.value = 'SWAP'
    return t

def t_KEY(t):
    r'KEY'
    t.value = 'KEY'
    return t

def t_SPACES(t):
    r'SPACES'
    t.value = 'SPACES'
    return t

def t_SPACE(t):
    r'SPACE'
    t.value = 'SPACE'
    return t

def t_CR(t):
    r'CR'
    t.value = 'CR'
    return t

def t_PRINTTEXT(t):
    r'\."[^"]*"'
    t.value = t.value[2:-1]
    return t

def t_PRINT(t):
    r'\.'
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_DUP(t):
    r'DUP'
    t.value = 'DUP'
    return t

def t_EMIT(t):
    r'EMIT'
    t.value = 'EMIT'
    return t

def t_FUNCTIONCALL(t):
    r'[a-zA-Z_][a-zA-Z_123456789]+'
    if (t.value in t.lexer.functions):
        return t
    else:
        raise Exception(f'Function {t.value} is not defined.')

t_ANY_ignore = ' \n\t'

def t_ANY_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex(reflags=re.I)
lexer.begin('INITIAL')

lexer.functions = []

file = """
:  hello-world ( -- )
 ." Hello, World!" cr ;
"""

lexer.input(file)

while tok := lexer.token():
    print(tok)