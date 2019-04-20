import sys
from inspect import getframeinfo, stack

asmheader = "DEFAULT REL\nextern _printf\nextern _scanf\nextern _fflush\nglobal _main\n"
asmtext = "section .text\n"
asmdata = 'section .data\n'
asmleave = 'mov rax, 0\npop rbp\nret\n'

reg_order = ["rdi", "rsi", "rdx", "rcx"]

global_var = []

global_str_counter = 0
global_str = {}
global_if_counter = 0
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

cmp_symbol = ['==', '!=', '>', '<', '>=', '<=', '&&']


def get_type(symbol):
    if type(symbol) is tuple:
        if symbol[0] == 'array':
            return 'ARRAY'
        return 'expression'
    if symbol == 'array':
        return 'ARRAY'
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
    caller = getframeinfo(stack()[1][0])
    print("Error line : " + str(caller.lineno))
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
        _text = ''
        if '\\n' in text:
            texts = text.replace('"', '').split('\\n')
            for t in texts:
                if t:
                    _text += '"' + t + '", 10,'
            _text += ' 0'
        else:
            _text = text + ', 0'
        add_data(asm_symbol, _text)
        global_str_counter += 1


def declare_arr(var_name, args):
    global asmdata
    if var_name in global_var:
        print_error("Duplicate variable")
    else:
        if args[0] == 'argument':
            asmdata += "%s dq " % var_name
            while args[1] != None:
                asmdata += "%s ," % args[1]
                args = args[2]
        else:
            # var array with size
            asmdata += "%s times %s dq 0" % (var_name, args)
        asmdata += '\n'


def multiple_stm_routine(stm1, stm2):
    statement_main(stm1)
    statement_main(stm2)


def ifelse_routine(ifstm, elsestm):
    if_routine(ifstm[1], ifstm[2], iselse=True)
    else_routine(elsestm)


def if_routine(exp, stm, iselse=False):
    global global_if_counter
    global_if_counter += 1
    exit_c = global_if_counter
    expression_main(exp)
    statement_main(stm)
    if iselse:
        add_text("jmp _L%d" % (global_if_counter + 1))
    add_text("_L%d:" % exit_c)


def else_routine(stm):
    global global_if_counter
    statement_main(stm[1])
    global_if_counter += 1
    add_text("_L%d:" % global_if_counter)


def while_routine(exp, stm):
    global global_if_counter
    loop_c = global_if_counter
    exit_c = loop_c + 1
    add_text("_L%d:" % loop_c)
    global_if_counter += 1
    expression_main(exp)
    global_if_counter += 1
    statement_main(stm)
    add_text("jmp _L%d" % loop_c)
    add_text("_L%d:" % exit_c)
    global_if_counter += 1


def statement_main(stm):
    state_symbol = stm[0]
    switcher = {
        'assign': assign_routine,
        'print': print_routine,
        'var_constant': declare_var,
        'var_array': declare_arr,
        'multiple_stm': multiple_stm_routine,
        'if': if_routine,
        'ifelse': ifelse_routine,
        'while': while_routine
    }
    func = switcher[state_symbol]
    func(stm[1], stm[2])


def expression_main(exp, count=0):
    t = exp[0]
    if t in cmp_symbol:
        cmp_main(exp)
    else:
        switcher = {
            '+': plus_routine,
            '-': minus_routine,
            '*': multiply_routine,
            '/': divide_routine,
            '%': mod_routine
        }

        func = switcher[t]
        func(exp[1], exp[2], count)


def cmp_main(cmp_e):
    global global_if_counter
    t = cmp_e[0]
    a = cmp_e[1]
    b = cmp_e[2]
    type_a = get_type(a)
    type_b = get_type(b)
    if type_a == 'expression':
        expression_main(a)
        add_text("mov rbx, rax")
    elif type_a == 'ID':
        add_text("mov rbx, [%s]" % a)
    elif type_a == 'CONSTANT':
        add_text("mov rbx, %s" % a)

    if type_b == 'expression':
        expression_main(b)
    elif type_b == 'ID':
        add_text("mov rax, [%s]" % b)
    elif type_b == 'CONSTANT':
        add_text("mov rax, %s" % b)
    # add_text("/////////////")
    # add_text(str(a))
    # add_text(str(b))
    if t != '&&':
        add_text("cmp rbx, rax")
    # add_text("/////////////")
    switcher = {
        '==': equal_routine,
        '>': greater_routine,
        '<': less_routine,
        '<=': less_equ_routine,
        '>=': greater_equ_routine,
        '&&': and_routine
    }
    func = switcher[t]
    func()


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
            elif a_type == 'ARRAY':
                index_type = get_type(a[2])
                if index_type == 'ID':
                    add_text('mov rbx, %s' % a[1])
                    add_text('mov rcx, [%s]' % a[2])
                    add_text('imul rcx, 8')
                    add_text('add rbx, rcx')
                    add_text('mov %s, [rbx]' % reg_order[reg_c])
                elif index_type == 'CONSTANT':
                    add_text('mov %s, [%s + %s * 8]' %
                             (reg_order[reg_c], a[1], a[2]))
            else:
                expression_main(arg[1])
                add_text("mov %s, rax" % reg_order[reg_c])
        reg_c += 1
        arg = arg[2]
    add_text("call _printf")
    add_text("xor rdi, rdi")
    add_text("call _fflush")


def assign_routine(dest, source):
    d_type = get_type(dest)
    s_type = get_type(source)
    if s_type == 'CONSTANT':
        add_text('mov rax, ' + source)
    elif s_type == 'ID':
        add_text('mov rax, [%s]' % source)
    elif s_type == 'expression':
        expression_main(source)
    elif s_type == 'INPUT':
        input_routine()
    if d_type == 'ARRAY':
        index_type = get_type(dest[2])
        if index_type == 'ID':
            add_text('mov rbx, %s' % dest[1])
            add_text('mov rcx, [%s]' % dest[2])
            add_text('imul rcx, 8')
            add_text('add rbx, rcx')
            add_text('mov [rbx], rax')
        elif index_type == 'CONSTANT':
            add_text('mov [%s + %s * 8], rax' % (dest[1], dest[2]))
    else:
        add_text('mov [%s], rax' % dest)


def plus_routine(a, b, count=0):
    a_type = get_type(a)
    b_type = get_type(b)
    if a_type == 'CONSTANT':
        if count == 0:
            add_text("mov rax, %s" % a)
        else:
            add_text("add rax, " + a)
    elif a_type == 'ID':
        if count == 0:
            add_text("mov rax, [%s]" % a)
        else:
            add_text("add rax, [%s]" % a)
    elif a_type == 'expression':
        expression_main(a, count)
    else:
        error_token()
    count += 1

    if b_type == 'CONSTANT':
        add_text("add rax, " + b)
    elif b_type == 'ID':
        add_text("add rax, [%s]" % b)
    elif b_type == 'expression':
        expression_main(b, count)
    else:
        error_token()


def minus_routine(a, b, count=0):
    a_type = get_type(a)
    b_type = get_type(b)
    if a_type == 'CONSTANT':
        if count == 0:
            add_text("mov rax," + a)
        else:
            add_text("sub rax, " + a)
    elif a_type == 'ID':
        if count == 0:
            add_text("mov rax, [%s]" % a)
        else:
            add_text("sub rax, [%s]" % a)
    elif a_type == 'expression':
        expression_main(a, count)
    else:
        error_token()

    count += 1

    if b_type == 'CONSTANT':
        add_text("sub rax, " + b)
    elif b_type == 'ID':
        add_text("sub rax, [%s]" % b)
    elif b_type == 'expression':
        expression_main(b, count)
    else:
        error_token()


def multiply_routine(a, b, count=0):
    a_type = get_type(a)
    b_type = get_type(b)
    if a_type == 'CONSTANT':
        if count == 0:
            add_text("mov rax," + a)
        else:
            add_text("imul rax, " + a)
    elif a_type == 'ID':
        if count == 0:
            add_text("mov rax, [%s]" % a)
        else:
            add_text("imul rax, [%s]" % a)
    elif a_type == 'expression':
        expression_main(a, count)

    count += 1

    if b_type == 'CONSTANT':
        add_text("imul rax, %s" % b)
    elif b_type == 'ID':
        add_text("imul rax, [%s]" % b)
    elif b_type == 'expression':
        expression_main(b, count)
    else:
        error_token()


def divide_routine(a, b, count=0):
    a_type = get_type(a)
    b_type = get_type(b)
    add_text('xor rdx, rdx')
    if a_type == 'CONSTANT':
        if count == 0:
            add_text('mov rax, ' + a)
        else:
            add_text('mov rcx, ' + a)
            add_text('idiv rcx')
    elif a_type == 'ID':
        if count == 0:
            add_text('mov rax, [%s]' % a)
        else:
            add_text('mov rcx, [%s]' % a)
            add_text('idiv rcx')
    elif a_type == 'expression':
        expression_main(a, count)

    count += 1

    add_text('xor rdx, rdx')
    if b_type == 'CONSTANT':
        add_text('mov rcx, ' + b)
        add_text('idiv rcx')
    elif b_type == 'ID':
        add_text('mov rcx, [%s]' % b)
        add_text('idiv rcx')
    elif b_type == 'expression':
        expression_main(b, count)


def mod_routine(a, b, count=0):
    a_type = get_type(a)
    b_type = get_type(b)
    add_text('xor rdx, rdx')
    if a_type == 'CONSTANT':
        if count == 0:
            add_text('mov rax, ' + a)
        else:
            add_text('mov rcx, ' + a)
            add_text('idiv rcx')
            add_text('mov rax, rdx')
    elif a_type == 'ID':
        if count == 0:
            add_text('mov rax, [%s]' % a)
        else:
            add_text('mov rcx, [%s]' % a)
            add_text('idiv rcx')
            add_text('mov rax, rdx')
    elif a_type == 'expression':
        expression_main(a, count)

    count += 1

    add_text('xor rdx, rdx')
    if b_type == 'CONSTANT':
        add_text('mov rcx, ' + b)
        add_text('idiv rcx')
        add_text('mov rax, rdx')
    elif b_type == 'ID':
        add_text('mov rcx, [%s]' % b)
        add_text('idiv rcx')
        add_text('mov rax, rdx')
    elif b_type == 'expression':
        expression_main(b, count)


def and_routine():
    pass


def less_equ_routine():
    add_text("jg _L%d" % global_if_counter)


def greater_equ_routine():
    add_text("jl _L%d" % global_if_counter)


def less_routine():
    add_text("jge _L%d" % global_if_counter)


def greater_routine():
    add_text("jle _L%d" % global_if_counter)


def not_equal_routine():
    add_text("je _L%d" % global_if_counter)


def equal_routine():
    add_text("jne _L%d" % global_if_counter)
