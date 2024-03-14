import json
import ply.lex as lex
from datetime import datetime

# List of token names.   This is always required
tokens = ("LISTAR",
        "SELECIONAR",
        "ITEM",
        "MOEDA",
        "EURO",
        "CENT",
        "COMA",
        "POINT",
        "SAIR"
        )

produtos = {}
with open('produtos.json') as f:
    produtosList = json.load(f)

produtos = {produto['cod']: produto for produto in produtosList}

# Regular expression rules for simple tokens
def t_LISTAR(t):
    r'LISTAR'
    
    print("cod |    nome      | quantidade  | preco")
    print("--------------------------------------------------")
    for produto in produtos.values():
        print(f"{produto['cod']}   {produto['nome']}     {produto['quant']}   {produto['preco']}")
    
    print("--------------------------------------------------\n")
    return t

def t_SELECIONAR(t):
    r'SELECIONAR'
    return t

def converter_para_moeda(valor):
    if valor < 1:
        centavos = int(valor * 100)
        return f"{centavos}c"
    else:
        euros = int(valor)
        centavos = int(round((valor - euros) * 100))  
        if centavos == 100:  
            euros += 1
            centavos = 0
        if centavos == 0:
            return f"{euros}e"
        else:
            return f"{euros}e{centavos}c"

def t_ITEM(t):
    r'[A-Z][0-9]{2}'
    id = t.value

    if id in produtos:
        if(t.lexer.saldo >= produtos[id]['preco'] and produtos[id]['quant'] > 0):
            print("Pode retirar o produto dispensado \"" + produtos[id]['nome']+"\"")
            t.lexer.saldo -= produtos[id]['preco']
            produtos[id]['quant'] -= 1

            print("Saldo = " + converter_para_moeda(t.lexer.saldo) + "\n")
        else:
            print("Saldo insuficiente para satisfazer o seu pedido ou quantidade insuficiente")
            print("Saldo = " + converter_para_moeda(t.lexer.saldo) + "; Pedido = " + converter_para_moeda(produtos[id]['preco']))
    else:
        print("Item inexistente")

    return t

def t_MOEDA(t):
    r'MOEDA'
    return t

def t_EURO(t):
    r'[0-9]+e'
    t.lexer.saldo += int(t.value[:-1])
    return t

def t_CENT(t):
    r'[0-9]+c'
    t.lexer.saldo += int(t.value[:-1])/100
    return t

def t_COMA(t):
    r','
    return t

def t_POINT(t):
    r'\.'
    print("Saldo = " + converter_para_moeda(t.lexer.saldo))
    return t

def trocos(valor):
    moedas_euros = {200: "2e", 100: "1e"}
    moedas_centavos = {50: "50c", 20: "20c", 10: "10c", 2: "2c", 1: "1c"}
    resultado = []

    euros = int(valor)  # Parte inteira do valor é o número de euros
    centavos = round((valor - euros) * 100)  # Parte decimal multiplicada por 100 é o número de centavos


    while euros > 0:
        if (euros - 2 >= 0):
            resultado.append(moedas_euros[200])
            euros -= 2
        else:
            resultado.append(moedas_euros[100])
            euros -= 1  

    # Adicionando as moedas de centavos
    for moeda in sorted(moedas_centavos.keys(), reverse=True):
        if centavos >= moeda:
            quantidade = centavos // moeda
            resultado.extend([moedas_centavos[moeda]] * quantidade)
            centavos -= quantidade * moeda

    return resultado

def contaOcorrencias(lista):
    ocorrencias = {}
    for item in lista:
        if item in ocorrencias:
            ocorrencias[item] += 1
        else:
            ocorrencias[item] = 1
    return ocorrencias

def t_SAIR(t):
    r'SAIR'

    if t.lexer.saldo != 0: 
        trocosP = trocos(t.lexer.saldo)
        print("Pode retirar o troco:")
        result = contaOcorrencias(trocosP)

        formatted_results = [f"{result[elem]}x {elem}" for elem in result]

        if len(formatted_results) > 1:
            print(', '.join(formatted_results[:-1]) + ' e ' + formatted_results[-1]+".")
        else:
            print(formatted_results[0])

    print("Até à próxima\n")

    t.lexer.should_stop = True
    return t

t_ignore = " \t"

def t_error(t):
    print("Símbolo desconhecido '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
lexer.saldo = 0
lexer.should_stop = False

data_atual = datetime.now()
d = data_atual.strftime("%Y-%m-%d")
print(d +", Stock carregado, Estado atualizado.")
print("Bom dia. Estou disponível para atender o seu pedido.")
while not lexer.should_stop:
    
    entrada = input("")
    lexer.input(entrada)
    for token in lexer:
        print(token)