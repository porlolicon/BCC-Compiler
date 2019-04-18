# BCC-Compiler
## Compiler Construction Assignment

## Syntax Example
```
  func sum(a, b){
    ret a + b
  }

  func main(){
    var a = 2
    var b = 3
    var c = sum(a, b)
    print("%d + %d = %d", a, b, c);
  }
```

## Build
```
  flex src/bcc.l
  gcc lex.yy.c src/main.c src/syscall.c src/util.c src/hash.c src/token.c
```

## Build with Makefile
```
  make clean
  make all
```

## Test
```
  # Linux
  ./a.out test.bcc output.asm
  
  # Windows
  ./a.exe test.bcc output.asm
```