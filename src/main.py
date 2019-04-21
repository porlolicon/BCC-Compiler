import argparse
import bcclex
import bccparse
import util
import subprocess
import platform

nasm_args = {'Linux': 'elf64', 'Darwin': 'macho64'}

system_platform = platform.system()

parser = argparse.ArgumentParser(description='Bcc compiler')
parser.add_argument("input", help="Path of file to compile.")
parser.add_argument("output_asm", help="Output assembly file name.")
parser.add_argument("output_exec", help="Output executeable file name.")
args = parser.parse_args()


lines = open(args.input, 'r').read()
util.lexer = bcclex.lexer
result = bccparse.parse(lines)
if result:
    util.statement_main(result)
    file = open(args.output_asm, 'w')
    file.writelines(util.asmheader)
    file.writelines(util.asmdata)
    file.writelines(util.asmtext)
    file.writelines(util.asmleave)
    file.close()

    if system_platform not in nasm_args:
        print("Compile to executeable for this platform is not supported yet.")
    else:
        nasm_arg = nasm_args[system_platform]
        p = subprocess.Popen(['nasm', '-f', nasm_arg, args.output_asm])
        p.wait()
        p = subprocess.Popen(
            ['gcc', '-w', '-no-pie', '-m64', '-o', args.output_exec, args.output_asm[:-3] + 'o'])
        p.wait()
        print("Compiled successfully.")
