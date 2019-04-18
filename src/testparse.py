import bcclex

tokens = bcclex.tokens

# statement --------------------------------


def p_statement_simple(p):
    '''statement : assignexp NEWLINE
                 | defineexp NEWLINE'''
    #  | printexp NEWLINE
    #  | inputexp NEWLINE
    #  | ifexp NEWLINE
    #  | loopexp NEWLINE
    p[0] = p[1]

# assignexp --------------------------------


def p_assignexp_simple(p):
    '''assignexp : ID "=" expression
                 | arrayG "=" expression'''
    p[0] = ("assign", p[1], p[3])

# define --------------------------------


def p_defineexp_constant1(p):
    'defineexp : VAR ID'
    p[0] = ("var_constant", p[2], 0)


def p_defineexp_constant2(p):
    'defineexp : VAR ID "=" expression'
    p[0] = ("var_constant", p[2], p[4])


def p_defineexp_array1(p):
    'defineexp : VAR ID "=" "{" arrayX "}"'
    p[0] = ("var_array", p[2], p[5])


def p_defineexp_array2(p):
    'defineexp : VAR ID "[" CONSTANT "]"'
    p[0] = ("var_array", p[2], p[4], 0)


def p_defineexp_array3(p):
    'defineexp : VAR ID "[" CONSTANT "]" "=" "{" arrayX "}"'
    p[0] = ("var_array", p[2], p[4], p[8])


def p_arrayX_simple(p):
    'arrayX : CONSTANT arrayY'
    p[0] = ("arrayX", p[1], p[2])


def p_arrayY_simple(p):
    '''arrayY : "," CONSTANT arrayY
              | empty empty empty'''
    p[0] = ("arrayY", p[2], p[3])


# def p_statement_var(p):
#     '''statement : VAR ID'''
#     p[0] = ('var', p[2])


# def p_statement_assign(p):
#     'statement : ID "=" expression'
#     p[0] = ('assign', p[1], p[3])


# def p_statement_if(p):
#     'statement : IF expression "{" statement "}"'
#     p[0] = ('if', p[2], p[4])


# def p_statement_while(p):
#     'statement : WHILE expression "{" statement "}"'
#     p[0] = ('while', p[2], p[4])


# Array gramma
def p_arrayG_simple(p):
    '''arrayG : ID "[" CONSTANT "]"
              | ID "[" ID "]"'''
    p[0] = ("array", p[1], p[3])

# Expression -----------------------------------------------


def p_expression_simple(p):
    '''expression : ID
                  | CONSTANT
                  | arrayG'''
    p[0] = p[1]

# boolean
#'EQ_OP', 'LE_OP', 'GE_OP', 'NE_OP' , 'AND_OP', 'OR_OP' , '<' , '>'


def p_expression_and(p):
    'expression : expression AND_OP expression'
    p[0] = ('&&', p[1], p[3])


def p_expression_or(p):
    'expression : expression OR_OP expression'
    p[0] = ('||', p[1], p[3])


def p_expression_EQ(p):
    'expression : expression EQ_OP expression'
    p[0] = ('==', p[1], p[3])


def p_expression_LE(p):
    'expression : expression LE_OP expression'
    p[0] = ('<=', p[1], p[3])


def p_expression_GE(p):
    'expression : expression GE_OP expression'
    p[0] = ('>=', p[1], p[3])


def p_expression_NE(p):
    'expression : expression NE_OP expression'
    p[0] = ('!=', p[1], p[3])


def p_expression_less(p):
    'expression : expression "<" expression'
    p[0] = ('<', p[1], p[3])


def p_expression_greaterthan(p):
    'expression : expression ">" expression'
    p[0] = ('>', p[1], p[3])

# math
# + - * / % -val ()


def p_expression_math(p):
    '''expression : expression "+" expression
                  | expression "-" expression
                  | expression "*" expression
                  | expression "/" expression
                  | expression "%" expression'''
    p[0] = (p[2], p[1], p[3])


def p_expression_minusValue(p):
    'expression : "-" expression'
    p[0] = ('minus', p[1])


def p_expression_bracket(p):
    'expression : "(" expression ")"'
    p[0] = ('bracket', p[2])


# -----------------------------------------------

def p_empty(p):
    'empty :'
    pass


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


import ply.yacc as yacc

parser = yacc.yacc()


def parse(s):
    return parser.parse(s)


while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s + '\n')
    print(result)
