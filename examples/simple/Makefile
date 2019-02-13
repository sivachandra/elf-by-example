all: with_glibc with_musl

CFLAGS = -fPIC -nostdinc
LDFLAGS = -static-pie -nostdlib -nostartfiles
STARTFILES = ../musl_install/lib/crti.o

with_glibc: main_glibc
	$(CC) 
