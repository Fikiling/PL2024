import ply.lex as lex
import sys
import re

# Token list
tokens = (
    "QUESTION_MARK",
    "EXCLAMATION_MARK",
    "EQUAL",
    "MULTIPLICATION",
    "DIVISION",
    "PLUS",
    "MINUS",
    "LPAREN",
    "RPAREN",
    "NUMBER",
    "ID"
)

# Token patterns
t_QUESTION_MARK = r'\?'
t_EXCLAMATION_MARK = r'!'
t_EQUAL = r'='
t_MULTIPLICATION = r"\*"
t_DIVISION = r"/"
t_PLUS = r"\+"
t_MINUS = r"-"
t_LPAREN = r"\("
t_RPAREN = r"\)"

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_ID(t):
    r'[a-zA-Z]\w*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignored characters
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_eof(t):
    r'\$'
    t.value = None 
    return t

lexer = lex.lex()