## What is a statically linked executable?

A statically linked executable is one which does not depend on any dynamically 
loaded libraries. Traditionally, a statically linked executable is also not a
[PIE](pie.md). Hence, the ELF file of a statically linked executable will not
have a `.dynamic` section. Further, since the executable is not a PIE, it will
not require any dynamic relocations to be applied. Hence, the ELF file of a
statically linked executable will also not have a `.dyn.rel[a]` sections.

Since a statically linked executable is not a PIE, one can do another
experiment using gdb: For different runs of the executable, after enabling
load address randomization in gdb, print the address of the `main` function.
The address should be the same for the different runs. In contrast with a
dynamically linked executable, the address will change for every run.

**NOTE**: To enable load address randomization in gdb, do this:

```
(gdb) set disable-randomization off
```
