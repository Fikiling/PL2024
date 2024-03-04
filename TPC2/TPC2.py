import re

def markdown_to_html(markdown):
    # Cabeçalhos
    markdown = re.sub(r'^(#{1,3})\s+(.+)\n$', r'^<h1> \2 </h1>', markdown, flags=re.MULTILINE)
     
    # Bold
    markdown = re.sub(r'\*\*([^*]+?)\*\*', r'^<b> \1 </b>', markdown)
    
    # Itálico
    markdown = re.sub(r'\*([^*]+?)\*', r'^<i> \1 </i>', markdown)
    
    # Lista numerada
    markdown = re.sub(r'', r'', markdown, flags=re.MULTILINE)
    
    #Lista não numerada
    markdown = re.sub(r'', r'', markdown)
    
    # Code
    markdown = re.sub(r'', r'', markdown)

    # Horizontal Rule
    markdown = re.sub(r'', r'', markdown)

    # Link
    markdown = re.sub(r'', r'', markdown)
    
    # Imagem
    markdown = re.sub(r'', r'', markdown)
    
    return markdown

# Exemplo de uso
markdown = '''
# Exemplo
Este é um **exemplo** ...
Este é um *exemplo* ...
1. Primeiro item
2. Segundo item
3. Terceiro item
Como pode ser consultado em [página da UC](http://www.uc.pt)
Como se vê na imagem seguinte: ![imagem dum coelho](http://www.coellho.com) ...
'''

html = markdown_to_html(markdown)
print(html)