import math
import decimal
from ply import lex, yacc


tokens = ('SECID', 'KEY', 'VALUE')
literals=("=", "[", "]")

def t_SECID(tok):
    r'(?<=\[)([a-zA-Z]+[0-9]?)' #only lowercase.
    tok.type="SECID"
    return tok

def t_KEY(tok):
    "(?<!=)(\w+)" #only lowercase.
    tok.type='KEY'
    return tok

def t_VALUE(tok):
    '''(?<=\=)(\w+)''' #only lowercase.
    tok.type="VALUE"
    #tok.value=tok.value[]
    return tok

def t_newline(tok):
    r'\n+'
    tok.lexer.lineno += tok.value.count("\n")

def t_error(tok):
    print("Illegal character %s"%tok.value[0])
    tok.lexer.skip(1)

t_ignore = " \t"

lexer= lex.lex()
input= """
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

lexer.input(input)
for tok in lexer:
    print(tok) #print tok.type, " => ", tok .value, "at (%d, %d)"%(tok.lineno, tok.lexpos)



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

p = yacc.yacc()
t=(p.parse(input, lexer=lexer))
from pprint import pprint
pprint(t)
ini={}
for tup in t:
    ini[tup[0]]=dict(tup[1])

pprint(ini)
