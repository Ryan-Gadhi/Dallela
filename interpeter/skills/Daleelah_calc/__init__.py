
import json
import sys
from adapt.intent import IntentBuilder
from interpeter.base import Skill, Handler
import os
import re


def grap_opr_func(opr):
    # TODO: elegant way to implement this crappy method

    add = lambda x,y: x + y
    sub = lambda x,y: x - y
    mul = lambda x,y: x * y
    div = lambda x,y: x / y
    pwr = lambda x,y: x ** y
    dflt = lambda x,y: x 
    opr = opr.strip()
    print(opr, 'is the operation')
    if re.search(r"(plus|add|\+)", opr): #to capture all occurances of different but similar format e.g: plused by
        return add
    elif re.search("(subtract|minus|-)", opr):
        return sub
    elif re.search("(mult|^by$|\*)", opr):
        return mul
    elif re.search("(div|on|/)", opr):
        return div
    elif re.search("(power|raise)", opr):
        return pwr
    return dflt

def plusFunc(eng_res):
    print(eng_res)
    expr = eng_res.get('n_kwd', None) #graps expression, e.g: 1 plus 2 minus 3
    p = r"(\d+)(\s*\D+\s*)*"
    n_opr = re.findall(p, expr) # [('1', 'plus'), ('2', 'minus)...]
    total, next_opration = None, None
    for n,opr in n_opr:
        if not next_opration: 
            total = int(n)
            next_opration = grap_opr_func(opr)
            continue
        total = next_opration(total, int(n))
        next_opration = grap_opr_func(opr)
    return {'result': total, 'n_kwd': eng_res['n_kwd']}
        




mapper = {
    "CalcIntent" : plusFunc,
}

class calcSkill(Skill):
    def __init__(self):
        super().__init__()
        
        for handler in self.handlers:
            handler.func = mapper.get(handler.intent.name, None) #if it has no function set None
        







def getSkill():
    return calcSkill()

