import re

texto = open('exemplo.txt', 'r').read()
ON = True
total = 0
for i, on, off, equ, skip, unk in re.findall(r'''
                                            ([+-]?\d+)  
                                        |   (on)  
                                        |   (off)  
                                        |   (=)  
                                        |   (\s+) 
                                        |   (.)  
                                        ''', texto, re.I|re.X):
    
    if equ: print ('Total = ', total)
    elif on: ON = True
    elif off: ON = False
    elif i and ON: total = total + int (i)
    elif skip: pass
    elif unk: pass



