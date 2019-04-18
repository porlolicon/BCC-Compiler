import sys

asmheader = "DEFAULT REL\nextern _printf\nextern _scanf\nextern _fflush\nglobal _main\n"
asmtext = "section .text\n"
asmdata = 'section .data\n'
asmleave = 'mov rax, 0\npop rbp\nret\n'

reg_order = ["rdi", "rsi", "rdx", "rcx"]

global_var = []

global_str_counter = 0
global_str = {}
str_prefix = '_LC'


def add_data(var_name, value):
    global asmdata
    asmdata += "%s db %s\n" % (var_name, value)


def add_text(cmd):
    global asmtext
    asmtext += cmd + '\n'


# init
# sys_input
add_data("_fmin", "\"%d\", 0")
add_text("_input:")
add_text("push rbp")
add_text("mov rbp, rsp")
add_text("sub rsp, 16")
add_text("lea rax, [rbp - 8]")
add_text("mov rsi, rax")
add_text("mov rdi, _fmin")
add_text("call _scanf")
add_text("mov rax, [rbp - 8]")
add_text("leave")
add_text("ret")

# add main label
add_text("_main:")
add_text("push rbp")

'''
I know this is stupid.
Just leave it alone.
'''
def get_type(symbol):
    if type(symbol) is tuple:
        return 'expression'
    if symbol == 'input':
        return 'INPUT'
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


def print_error(error_str):
    print("ERROR : " + error_str)


def error_token():
    print_error("Unexpected token")


def declare_var(var_name, value=0):
    global asmdata
    if var_name in global_var:
        print_error("Duplicate variable")
    else:
        if value == 'input':
            asmdata += "%s dq 0\n" % var_name
            input_routine()
            add_text("mov [%s], rax" % var_name)
        else:
            asmdata += "%s dq %s\n" % (var_name, value)


def declare_string(text):
    global global_str_counter
    if text not in global_str:
        asm_symbol = str_prefix + str(global_str_counter)
        global_str[text] = asm_symbol
        asm_val = '%s, 0' % text
        add_data(asm_symbol, asm_val)
        global_str_counter += 1


def declare_arr(var_name, args):
    global asmdata
    if var_name in global_var:
        print_error("Duplicate variable")
    else:
        asmdata += "%s dq " % var_name
        if args[0] == 'argument':
            while args[1] != None:
                asmdata += "%s ," % args[1]
                args = args[2]
        asmdata += '\n'


def statement_main(stm):
    state_symbol = stm[0]
    switcher = {
        'assign': assign_routine,
        'print': print_routine,
        'var_constant': declare_var,
        'var_array': declare_arr
    }
    func = switcher[state_symbol]
    func(stm[1], stm[2])


def expression_main(exp, count=0):
    t = exp[0]
    switcher = {
        '+': plus_routine,
        '-': minus_routine,
        '==': equal_routine
    }

    func = switcher[t]
    func(exp[1], exp[2], count)


def input_routine():
    add_text("call _input")


def print_routine(fmt, arg):
    add_text("mov rdi, " + get_str(fmt))
    reg_c = 1
    while arg[1] != None:
        if arg[0] == 'argument':
            a = arg[1]
            a_type = get_type(a)
            if a_type == 'CONSTANT':
                add_text("mov %s, %s" % (reg_order[reg_c], a))
            elif a_type == 'ID':
                add_text("mov %s, [%s]" % (reg_order[reg_c], a))
            else:
                expression_main(arg[1])
                add_text("mov %s, rax" % reg_order[reg_c])
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
    elif s_type == 'INPUT':
        input_routine()
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


def equal_routine(a, b):
    print("EQ ROUTINE")
