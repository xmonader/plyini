import math
import decimal
from pprint import pprint

from ply import lex, yacc


tokens = ('SECID', 'KEY', 'VALUE')
literals=("=", "[", "]")

def t_SECID(tok):
    r'(?<=\[)([a-zA-Z]+[0-9]?)'
    tok.type="SECID"
    return tok

def t_KEY(tok):
    "(?<!=)(\w+)"
    tok.type='KEY'
    return tok

def t_VALUE(tok):
    '''(?<=\=)(\w+)'''
    tok.type="VALUE"
    return tok

def t_newline(tok):
    r'\n+'
    tok.lexer.lineno += tok.value.count("\n")

def t_error(tok):
    print("Illegal character %s"%tok.value[0])
    tok.lexer.skip(1)

t_ignore = " \t"

#GRAMMAR::
# inifile: sectionsdef
#
# sectionsdef : sectiondef sectionsdef
#             |
#
# sectiondef :
#             [SEC]
#             keyvaluedefs
#
# keyvaluedefs  : keyvaluedef keyvaluedefs
#               |
#
# keyvaluedef :
#         key = value

def p_inifile(p):
    "inifile : sectionsdef"
    p[0]=p[1]

def p_sectionsdef(p):
    """
    sectionsdef : sectiondef sectionsdef
                |
    """
    sections = []
    if len(p) == 2:
        sections.append(p[1])
    if len(p) > 2:
        for el in [p[1], p[2]]:
            if isinstance(el, list):
                sections.extend(el)
            else:
                sections.append(el)

    p[0] = sections

def p_sectiondef(p):
    """
    sectiondef : "[" SECID "]" keyvaluedefs
    """
    if len(p) == 5:
        p[0] = (p[2], p[4])

def p_keyvaluedefs(p):
    """
    keyvaluedefs : keyvaluedef keyvaluedefs
                 |
    """
    binds = []
    if len(p)==2:
        binds.append(p[1])

    if len(p)>2:
        for el in [p[1], p[2]]:
            if isinstance(el, list):
                binds.extend(el)
            else:
                binds.append(el)

    p[0] = binds

def p_keyvaluedef(p):
    """keyvaluedef : KEY "=" VALUE"""
    keyval = (p[1], p[3])

    p[0]= keyval

def p_error(p):
    print("Syntax error", p)

def asdict(s):
    lexer= lex.lex()

    # lexer.input(s)
    # for tok in lexer:
    #     print(tok) #print tok.type, " => ", tok .value, "at (%d, %d)"%(tok.lineno, tok.lexpos)
    p = yacc.yacc()
    t=(p.parse(s, lexer=lexer))
    #pprint(t)
    ini={}
    for tup in t:
        ini[tup[0]]=dict(tup[1])

    return ini
if __name__ == "__main__":


    s = """
[Sec1]
k1=v1
k2=v2
[Sec2]
k3=v3
k4=v4
[Sec4]
k5=sahme
k6=9
k1=21
    """
    ini = asdict(s)
    pprint(ini)
