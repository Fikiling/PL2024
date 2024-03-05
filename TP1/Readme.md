# TPC1 

## Objetivo

Processar um dataser em CSV e processá-lo sem uso da biblioteca csv


### Raciocínio

1. Mudar para a diretoria com o dataset com o módulo 'os' do    pyhton. 

2. Abrir o csv em modo de leitura e fazer o respetivo parse dos valores, foi usada para cada linha a função split com o uso do ';' que é o símbolo definido para separação de campo do CSV e os dados foram processados.

3. Em seguida são inicializadas as variavéis:
   - `modalidades` é uma lista vazia usada para armazenar as modalidades.
   - `aptos` e `inaptos` contadores do o número de registos com resultado "true" e "false", respectivamente.
   - `escalaoEtario` é um dicionário vazio que será usado para conter os atletas distribuídos por faixa etária.

4. Os valores relevantes são extraídos da linha usando índices específicos:
   - `id` recebe o valor do primeiro elemento (índice 0).
   - `nome` é construído concatenando os valores do terceiro (índice 3) e quarto (índice 4) elementos.
   - `resultado` recebe o valor do último elemento (índice -1).
   - `idadeS` recebe o valor do quinto elemento (índice 5).
   - `idade` é convertida para um número inteiro usando `int(values[5])`.
   - `genero`, `morada`, `modalidade`, `clube`, `email` e `fed` recebem os valores dos elementos correspondentes.

5. O dicionário criado que representa a faixa etária com base na idade, é criado da seguinte maneira:
    - se a `idade` for 25, o índice será "[20-24]". 

6. Após o parsing de todo o ficheiro CSV, a lista `modalidades` é ordenada por ordem alfabética

