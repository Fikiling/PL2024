import os 

##TODO 

## Lista ordenada alfabeticamente das modalidades desportivas;
## Percentagens de atletas aptos e inaptos para a prática desportiva;
## Distribuição de atletas por escalão etário (escalão = intervalo de 5 anos): ... [30-34], [35-39], ...


os.chdir('../../Sets/')

with open('emd.csv', 'r') as file:
    
    modalidades = []
    aptos = 0
    inaptos = 0
    escalaoEtario= {}

    lines = file.readlines()

    #_id,index,dataEMD,nome/primeiro,nome/último,idade,género,morada,modalidade,clube,email,federado,resultado
    for line in lines[1:]:
        values = line.strip().split(',')

        id = values[0]
        nome = values[3] + " " + values[4]
        resultado = values[-1]
        idadeS = values[5]
        idade = int(values[5])        
        genero = values[6]
        morada = values[7]
        modalidade = values[8]
        clube = values[9]
        email = values[10]
        fed = values[11]
        
        if modalidade not in modalidades:
            modalidades.append(modalidade)
        
        if resultado == 'true':
            aptos += 1
        
        else:
            inaptos += 1
            
        escalao = f'[{idade// 5*5}-{idade//5*5+4}]'
        
        if escalao not in escalaoEtario:
            escalaoEtario[escalao] = [{"nome": nome, "idade": idadeS, "genero": genero, "morada":morada, 
                                "modalidade": modalidade, "clube": clube, "fed": fed}]
        else:
            escalaoEtario[escalao][len(escalaoEtario[escalao]):] = [{ "nome": nome, "idade": idadeS, "genero": genero, "morada":morada, 
                                                             "modalidade": modalidade, "clube": clube, "fed": fed}]



modAlfabetizadas = sorted(modalidades)    
print("Lista ordenada alfabeticamente das modalidades desportivas:")
for elem in modAlfabetizadas:
    print (f'-{elem}')

print(f"Percentagem de atltetas inaptos: {inaptos/(aptos+inaptos) * 100} %")
print(f"Percentagem de atltetas aptos:   {aptos/(aptos+inaptos) * 100} %")


print('Atletas distriubuídos por escalão etário')
for escalao, atletas in escalaoEtario.items():
    print(f"Escalão: {escalao}")
    for atleta in atletas:
        print(atleta)
    print('\n')
