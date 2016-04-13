""" This will parse a data file from material strength testing
    The data collection software saved data for applied load, piston displacement, two extensometers, and time
    We didn't have anything plugged into the extension channels, and we don't need time for analysis
    For this reason we're only printing out the load-displacement data in two comma-separated columns that can be copied
    Copying these two columns is a lot easier than copying all 5 columns and deleting 3 columns one line at a a time
    We're throwing out the column headers because we dont need them (and the units for load are wrong in the file)
    WARNING: This prints a lot of lines, so you might want to use head -15 instead of cat to run the parser
"""

tokens = ('LOAD','INTEGER','TAB')
literals = ['.','-']

# Tokens
t_LOAD  = r'Load.*'
t_TAB = r'\t'

#This parser can work with negative numbers as well
def t_INTEGER(t):
    r'-?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex   # ply.lex comes from the ply folder in the PLY download.
lexer = lex.lex()

# Parsing rules

global time_step
time_step = 0

def p_start(t):
    '''start : load
             | data
    '''

def p_load(t):
    'load : LOAD'

def p_data(t):
    'data : float TAB float TAB float TAB float TAB float'
    print(str(t[1]) + ", " + str(t[3]))

def p_float(t):
    'float : INTEGER "." INTEGER'
    t[0] =  str(t[1]) + str(t[2]) + str(t[3])

def p_error(t):
    if t == None:
        print("Syntax error at '%s'" % t)
    else:
        print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc   # ply.yacc comes from the ply folder in the PLY download.
parser = yacc.yacc()

while True:
    try:
        s = input('')
    except EOFError:
        break
    parser.parse(s)

# To run the parser for fewer lines in the file: head -15 plyParserInputs/bass_bending | python P5Parser.py
# To run the parser do the following in a terminal window: cat plyParserInputs/bass_bending | python P5Parser.py
