import re 



text = 'Este é um **exemplo** e agora **outro** exemplo.'
print(re.sub(r'\*\*([^*]+?)\*\*', r'^<b> \1 </b>', text))