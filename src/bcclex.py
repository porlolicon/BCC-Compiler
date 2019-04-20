import ply.lex as lex
tokens = ['ID', 'CONSTANT', 'AND_OP', 'OR_OP', 'STRING_LITERAL',
          'EQ_OP', 'LE_OP', 'GE_OP', 'NE_OP', 'NEWLINE']

reserved = {
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'print': 'PRINT',
    'input': 'INPUT',
    'var': 'VAR'
}

tokens += reserved.values()

t_ignore = ' \t\v\f'
t_AND_OP = r'&&'
t_OR_OP = r'[||]'
t_LE_OP = r'<='
t_GE_OP = r'>='
t_EQ_OP = r'=='
t_NE_OP = r'!='
t_STRING_LITERAL = r'\"(\\.|[^"\\])*\"'


literals = ['{', '}', '[', ']', '=', ',', '>',
            '<', '!', '(', ')', '+', '-', '*', '/', '%', '"']


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_error(t):
    print('Illegal character')
    t.lexer.skip(1)


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = 'NEWLINE'
    return t


def t_CONSTANT(t):
    r'0h\d+|\d+|-\d+'
    if t.value[:2] == '0h':
        t.value = str(int(t.value.replace('0h', '0x'), 16))
    t.type = 'CONSTANT'
    return t


lexer = lex.lex()
