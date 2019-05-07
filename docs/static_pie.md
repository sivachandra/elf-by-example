## What is a static-pie linked executable?

A _static-pie_ linked executable is a fully statically linked executable which
is also a [PIE](pie.md). Since it is fully statically linked, it does not depend
on any dynamically loaded libraries. However, since it is a [PIE](pie.md), the
ELF file will have both the `.dynamic` and the `.rel[a].dyn` sections. 

The reason for requiring dynamic relocations (those in `.rel[a].dyn`) in a
static-pie binary are explained in
[this example.](https://github.com/sivachandra/elf-by-example/tree/master/examples/global_var_ptr)

A statically linked PIE binary differs from a dynamically linked PIE binary in
the following ways:

1. As there are no dynamic libraries to be loaded, they is no need of the
program interpreter. Consequently, there is no `PT_INTERP` segment in a
static-pie binary.
1. The dynamic section will not have `DT_NEEDED` entries as a static-pie binary
does not _need_ any dynamically loaded libraries.
