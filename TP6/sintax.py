from lex import lexer
import ply.lex as lex


next_symbol=("Error", "",0,0)

# Function to handle parser errors
def parserError(s):
    print("Syntax error:", s)

# Function to consume a terminal symbol
def consume_term(symbol):
    global next_symbol
    if next_symbol.type == symbol:
        next_symbol = lexer.token()
    else:
        parserError(symbol)

# Function to parse the language
def parse_language():
    global next_symbol
    if next_symbol.type == "QUESTION_MARK":
        consume_term("QUESTION_MARK")
        consume_term("ID")
        print("Parsed P1: Language -> ? id")
    elif next_symbol.type == "EXCLAMATION_MARK":
        consume_term("EXCLAMATION_MARK")
        parse_content()
        print("Parsed P2: Language -> ! Content")
    elif next_symbol.type == "ID":
        consume_term("ID")
        consume_term("EQUAL")
        parse_content()
        print("Parsed P3: Language -> id = Content")
    else:
        parserError(next_symbol)

# Function to parse content
def parse_content():
    global next_symbol
    if next_symbol.type == "ID":
        consume_term("ID")
        parse_rest()
        print("Parsed P4: Content -> id Rest")
    elif next_symbol.type == "NUMBER":
        consume_term("NUMBER")
        parse_rest()
        print("Parsed P5: Content -> num Rest")
    elif next_symbol.type == "LPAREN":
        consume_term("LPAREN")
        parse_content()
        consume_term("RPAREN")
        print("Parsed P6: Content -> ( Content )")
    else:
        parserError(next_symbol)

# Function to parse the rest
def parse_rest():
    global next_symbol
    if next_symbol.type in ["PLUS", "MINUS", "MULTIPLICATION", "DIVISION"]:
        consume_term(next_symbol.type)
        parse_content()
        print(f"Parsed P7-P10: Rest -> {next_symbol.type} Content")
    elif next_symbol.type in ["eof", "RPAREN"]:
        print("Parsed P11: Rest -> &")
    else:
        parserError(next_symbol)

# Function to start the parser
def start_parser(data):
    global next_symbol
    lexer.input(data)
    next_symbol = lexer.token()
    parse_language()
    print("Everything is fine")

# Test Program
l1 = "z = x * y + 10"
l2 = "! x * 2 + y"
l3 = "? x"
l4 = "y = (30 - 5) / x * 4 "

start_parser(l1)
start_parser(l2)
start_parser(l3)
start_parser(l4)