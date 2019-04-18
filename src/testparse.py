import bccparse

while True:
    try:
        s = input('[cmd] :')
    except EOFError:
        break
    if not s:
        continue
    result = bccparse.parse(s + '\n')
    print(result)