import bcclex
import bccparse
import util


lines = open('test.bcc', 'r').read()
result = bccparse.parse(lines)
util.statement_main(result)
print(util.asmheader)
print(util.asmdata)
print(util.asmtext)
print(util.asmleave)
