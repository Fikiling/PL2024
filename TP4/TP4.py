#Select id, nome, salario From empregados Where salario >= 820

import ply.lex as lex

# Lista de tokens

keywords = ( 'Select', 
            'Where', 
            'From' 
            )

tokens = keywords + (
    'ID',
    'NUMBER',
    'COMMA',
    'GREATER',
    'LESS',
    'EQUAL'

)

def t_Select(t):
    r'Select'
    return t

def t_Where(t):
    r'Where'
    return t

def t_From(t):
    r'From'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_COMMA = r','
t_GREATER = r'>'
t_LESS = r'<'
t_EQUAL = r'='

# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Carater desconhecido '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

print("Digite a expressão: ")
data = input()

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

