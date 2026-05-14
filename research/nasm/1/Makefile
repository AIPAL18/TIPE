FILE := main.asm
OBJ := main.o
EXE := main.exe

all: run

assemble:
	nasm -f elf64 $(FILE) -o $(OBJ)

disassemble_all:
	@echo "objdump -Mintel -D $(EXE)" 
	@echo "---------------"
	@objdump -Mintel -D $(EXE)
	@echo
	@echo "---------------"

disassemble:
	@echo "objdump -Mintel -d $(EXE)" 
	@echo "---------------"
	@objdump -Mintel -d $(EXE)
	@echo
	@echo "---------------"

link:
	ld -m elf_x86_64 $(OBJ) -o $(EXE)

run: assemble link
	@echo "---------------"
	@echo
	@./$(EXE)
	@echo
	@echo "---------------"
