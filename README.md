# BCC-Compiler
## Compiler Construction Assignment

## Syntax Example
```
var arr[10]
var i = 0

while i < 10 {
  print("[%ld]: ", i)
  arr[i] = input
  i = i + 1
}
i = 1
var min = arr[0]
while i < 10 {
  if arr[i] < min {
    min = arr[i]
  }
  i = i + 1
}
print("min: %ld\n" ,min)
```

```
# Timer program
var min = 0
var sec = 0
print("Timer\n")
while 1 == 1 {
  print("%.2ld:%.2ld\n", min, sec)
  sec = sec + 1
  if sec == 60 {
    sec = 0
    min = min + 1
  }
  # Sleep 1000 millisec
  sleep(1000)
}
```

## Prerequisite
* gcc for windows use [Mingw64](https://mingw-w64.org/doku.php/download/mingw-builds)
* nasm
* python 3

## Usage
```
python3 src/main.py source.bcc a.asm a.out
```
