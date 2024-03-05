# TPC2 

## Objetivo

**Conversor de MD para HTML**


### Raciocínio  


**Cabeçalhos:**
    
    Procurar por linhas começadas com "#" e substituir o "#" pelo "<h1>" correspondente e adicionar "</h1>" no final da linha.

**Bold:**
    
    Procurar por palavras começadas e acabas em "**" e substituir os "**" por "<b>" e "</b>".
    
**Itálico:**

    Procurar por palavras começadas e acabas em "*" e substituir os "*" por "<i>" e "</i>".

**Lista numerada:**

    Procurar por linhas começadas por inteiros seguidos por um "."  e substituir os inteiros por "<li>" e "</li>".
    De seguida procurar as linhas que começam por <li> e acabam em </li> e adicionar <ol> no início de cada bloco de list items </ol> no fim do bloco
    
**Imagem:**
    
    Procurar por conjuntos começados "![nome](path)" e usar os grupos de captura nome e path para substituir por "<img src="path" alt="nome">
    

**Link:**

    Procurar por conjuntos começados "[nome](path)" e usar os grupos de captura nome e path para substituir por "<a href="path" alt="nome">
    


***Nota**: é importante procurar primeiro por imagens e depois por links caso contrário o grupo de captura dos links vai encontrar os das imagens e depois quando formos procurar por imagens não vão existir porque já foram alterados pelos dos links*
  