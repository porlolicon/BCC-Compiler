import sys

asmheader = "DEFAULT REL\nextern _printf\nextern _scanf\nextern _fflush\nglobal _main\n"
asmtext = "section .text\n_main:\n"
asmdata = "section .data\n"

reg_order = ["rdi", "rsi", "rdx", "rcx"]

global_var = []
global_str_counter = 0
global_str = {}
str_prefix = '_LC'

# I know this is stupid.
# Just leave it alone.


def get_type(symbol):
    if type(symbol) is tuple:
        return 'expression'
    try:
        int(symbol)
        return 'CONSTANT'
    except ValueError:
        return 'ID'


def get_var(symbol):
    if symbol in global_var:
        return symbol

    print_error("Use of undeclare variable")
    sys.exit(1)


def get_str(text):
    if text not in global_str:
        declare_string(text)
    return global_str[text]


def add_data(var_name, value):
    global asmdata
    asmdata += "%s db %s\n" % (var_name, value)


def add_text(cmd):
    global asmtext
    asmtext += cmd + '\n'


def print_error(error_str):
    print("ERROR : " + error_str)


def error_token():
    print_error("Unexpected token")


def declare_var(var_name, value=0):
    if var_name in global_var:
        print_error("Duplicate variable")
    else:
        add_data(var_name, value)


def declare_string(text):
    if text not in global_str:
        asm_symbol = str_prefix + str(global_str_counter)
        global_str[text] = asm_symbol
        asm_val = '%s, 0' % text
        add_data(asm_symbol, asm_val)


def statement_main(stm):
    state_symbol = stm[0]
    switcher = {
        'assign': assign_routine,
        'print': print_routine
    }
    func = switcher[state_symbol]
    func(stm[1], stm[2])


def expression_main(exp, count=0):
    t = exp[0]
    switcher = {
        '+': plus_routine,
        '-': minus_routine
    }

    func = switcher[t]
    func(exp[1], exp[2], count)


def print_routine(fmt, arg):
    add_text("mov rdi, " + get_str(fmt))
    reg_c = 1
    while arg[1] != None:
        a = arg[1]
        a_type = get_type(a)
        if a_type == 'CONSTANT':
            add_text("mov %s, %s" % (reg_order[reg_c], a))
        elif a_type == 'ID':
            add_text("mov %s, [%s]" % (reg_order[reg_c], a))
        else:
            pass
        reg_c += 1
        arg = arg[2]
    add_text("call _printf")
    add_text("xor rdi, rdi")
    add_text("call _fflush")


def assign_routine(dest, source):
    s_type = get_type(source)
    if s_type == 'CONSTANT':
        add_text('mov rax, ' + source)
        add_text('mov [%s], rax' % dest)
    elif s_type == 'ID':
        add_text('mov rax, [%s]' % source)
        add_text('mov [%s], rax' % dest)
    elif s_type == 'expression':
        expression_main(source)
        add_text('mov [%s], rax' % dest)


def plus_routine(a, b, count=0):
    if count == 0:
        add_text("mov rax, 0")
    count += 1
    a_type = get_type(a)
    b_type = get_type(b)
    if a_type == 'CONSTANT':
        add_text("add rax, " + a)
    elif a_type == 'ID':
        add_text("add rax, [%s]" % a)
    else:
        error_token()

    if b_type == 'CONSTANT':
        add_text("add rax, " + b)
    elif b_type == 'ID':
        add_text("add rax, [%s]" % b)
    elif b_type == 'expression':
        expression_main(b, count)
    else:
        error_token()


def minus_routine(a, b, count=0):
    if count == 0:
        add_text("mov rax, 0")
    count += 1
    a_type = get_type(a)
    b_type = get_type(b)
    if a_type == 'CONSTANT':
        add_text("sub rax, " + a)
    elif a_type == 'ID':
        add_text("sub rax, [%s]" % a)
    else:
        error_token()

    if b_type == 'CONSTANT':
        add_text("sub rax, " + b)
    elif b_type == 'ID':
        add_text("sub rax, [%s]" % b)
    elif b_type == 'expression':
        expression_main(b, count)
    else:
        error_token()
