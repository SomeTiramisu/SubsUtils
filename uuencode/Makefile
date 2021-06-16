CFLAGS = -O3 -static -march=native -flto
OFLAGS = -O3

cuuencode:
	cc -o cuuencode cuuencode.c $(CFLAGS)
ouuencode:
	ocamlopt -o ouuencode ouuencode.ml $(OFLAGS)
ruuencode:
	rustc -o ruuencode ruuencode.rs

clean:
	rm cuuencode ouuencode ruuencode
