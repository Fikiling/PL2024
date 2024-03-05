import re

texto = 'Como pode ser consultado em [página da UC](http://www.uc.pt)'

out = 'Como pode ser consultado em <a href="http://www.uc.pt">página da UC</a>'
#result = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', texto)
result= re.sub(r'\[(.*?)\]\(http:\/\/(\w+\.*)+\)', r'<a href="\2">\1</a>', texto)

print(result)