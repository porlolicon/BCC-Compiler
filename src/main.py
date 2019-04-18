import bcclex
import bccparse
import util

try:
    lines = open('test.bcc','r').read()

    result = bccparse.parse(lines + '\n')
    if result:
        util.statement_main(result)
        print(util.asmheader)
        print(util.asmdata)
        print(util.asmtext)
        print(util.asmleave)
except:
    pass

while True:
    try:
        line = input("[cmd] : ")
    except EOFError:
        raise SystemExit
    result = bccparse.parse(line + '\n')
    if result:
        print(result)
        util.statement_main(result)
        print(util.asmheader)
        print(util.asmdata)
        print(util.asmtext)
        print(util.asmleave)