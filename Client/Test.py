'''
Created on 10 dic 2016

@author: Conny
'''
size=3
s=[]
for i in range(0,100):
    s.append(i)
    if len(s)>size:
        s=s[len(s)-size:]
    print(s)

