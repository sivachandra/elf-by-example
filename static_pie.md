## What is a static-pie linked executable?

Like a [statically linked executable](static.md) a static-pie linked executable
also does not depend on any dynamically loaded libraries. However, since it is
a PIE, the ELF file will have both the `.dynamic` and the `.rel[a].dyn`
sections. The reason for requiring dynamic relocations (those in `.rel[a].dyn`)
in a static-pie binary are explained in [this example.](https://github.com/sivachandra/elf-by-example/tree/master/examples/global_var_ptr)

In contract with a dynamically linked PIE, there are a few differences:

1. It will not have a `INTERP`segment. As there are no dynamic libraries to be
loaded, they is no need of the program interpreter.
1. The dynamic section will not have `DT_NEEDED` entries as a static-pie binary
does not depend on any dynamically loaded libraries.
