import bccparse

lines = open('test.bcc', 'r').read()

print(bccparse.parse(lines + '\n', debug=True))


while True:
    try:
        s = input('[cmd] :')
    except EOFError:
        break
    if not s:
        continue
    result = bccparse.parse(s + '\n')
    print(result)
