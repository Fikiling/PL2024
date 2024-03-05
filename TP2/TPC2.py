import re

def markdown_to_html(markdown):
    # Cabeçalhos
    markdown = re.sub(r'^#(.*?)$', r'<h1>\1</h1>', markdown, flags=re.MULTILINE)
    markdown = re.sub(r'^##(.*?)$', r'<h2>\1</h2>', markdown, flags=re.MULTILINE)
    markdown = re.sub(r'^##(.*?)$', r'<h3>\1</h3>', markdown, flags=re.MULTILINE)
    

    # Bold
    markdown = re.sub(r'\*\*(([^*]+?)\*?)*\*\*', r'<b> \2 </b>', markdown)
    
    # Itálico
    markdown = re.sub(r'\*([^*]+?)\*', r'<i> \1 </i>', markdown)
    
    # Lista numerada
    markdown = re.sub(r"^[0-9]+\.(.+)$", r"\t<li>\1</li>", markdown, flags = re.MULTILINE)
    markdown = re.sub(r"((\t<li>.+</li>\n)+)", r"<ol>\n\1</ol>\n", markdown, flags = re.MULTILINE)
    
    # Imagem
    markdown = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1">', markdown)

    # Link
    markdown = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', markdown)
    
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