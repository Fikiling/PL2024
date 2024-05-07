counter_do = 0
delimitadores_do = {}

with open("input.txt", "r") as file:
    codigo = file.read()

for linha in codigo.split('\n'):
    counter_do += linha.lower().count('do') 


for elem in range(counter_do):
    primeiro = (elem + 1)  * 2 - 2
    segundo = primeiro + 1
    delimitadores_do[elem + 1] = (primeiro, segundo)

vars = ''
for elem in range(counter_do):
    vars += '\tpushi 0\n'
    vars += '\tpushi 0\n'



print("Quantidade de do's encontrados:", counter_do)
print("Delimitadores gerados:", delimitadores_do)



'''
: func1 if ." Sucesso1" CR else ." Falha1" CR then ;
1 func1

: func2 if ." Falha2" CR else ." Sucesso2" CR then ;
0 func2

: func3 if ." Sucesso3" CR then ;
1 func3

: func4 if ." Falha4" CR then ." Sucesso4" CR ; 
0 func4

: func5 if if ." Sucesso5" CR else ." Falha5" CR then ." Sucesso5" CR then ." Sucesso5" CR ;
1 1 func5

-----------------------------------------------------------------------------------------------------

: faz ( -- )
    5 1 DO
        ." ola"
    LOOP ;
faz

-----------------------------------------------------------------------------------------------------

: sum ( n -- sum )
 0 swap 1 do
 i +
 loop ;

5 sum .


'''