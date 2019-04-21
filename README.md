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
