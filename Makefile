EXECFILE 				:=
NASM_ARC				:=
ifeq ($(OS),Windows_NT)
	EXECFILE = a.exe
	NASM_ARC = win64
else
	EXECFILE = a.out
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		NASM_ARC = elf64
	endif
	ifeq ($(UNAME_S),Darwin)
		NASM_ARC = macho64
	endif
endif

asm:
	@nasm -f $(NASM_ARC) test.asm
	@gcc -no-pie -m64 -o test.out test.o

clean:
	@rm -rf $(EXECFILE)
	@rm -rf test.o
	@rm -rf test.out

