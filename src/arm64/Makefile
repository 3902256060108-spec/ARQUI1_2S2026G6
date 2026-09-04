all: main

main: main.o
	ld -o main main.o

main.o: main.s
	as -g -o main.o main.s

clean:
	rm -f main main.o