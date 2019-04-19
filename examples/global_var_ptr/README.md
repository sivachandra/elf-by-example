# `.rel.dyn` relocations in static-pie

Normally, in statically linked executables, one does not expect to any dynamic
relocations (the relocations which are listed in the `.rel.dyn` section.)
However, since static-pie is infact a PIE, a bunch of relocations will have to
be applied by the CRT at startup. For `x86_64`, such relocations are of type
`R_X86_64_RELATIVE`. For static-pie, they are typically required if there is a
global variable holding the address of another global var. Since the address of
global variables at runtime will depend on the load address of the executable,
the relocations of type `R_X86_64_RELATIVE` instruct the CRT to adjust their
addresses based on the executable's load address.

The example in this directory helps us see the need for the above relocations.
In `main.c`, we have two global variables, `global_int` and `global_int_ptr`.
The variable `global_int_ptr` holds the address of `global_int`. If we look at
the readelf dump of
`out/examples/global_var_ptr/global_var_ptr.clang.musl.ld.lld`, we have this:

```
Relocation section '.rela.dyn' at offset 0x248 contains 6 entries:
    Offset             Info             Type               Symbol's Value  Symbol's Name + Addend
0000000000003008  0000000000000008 R_X86_64_RELATIVE                         3000
0000000000003010  0000000000000008 R_X86_64_RELATIVE                         3010
0000000000002000  0000000000000008 R_X86_64_RELATIVE                         1240
0000000000002008  0000000000000008 R_X86_64_RELATIVE                         1280
0000000000002148  0000000000000008 R_X86_64_RELATIVE                         2010
0000000000002150  0000000000000008 R_X86_64_RELATIVE                         2000
```

The symbol table has this:

```
Symbol table '.symtab' contains 79 entries:
   Num:    Value          Size Type    Bind   Vis      Ndx Name
   .....
    57: 0000000000003000     4 OBJECT  GLOBAL DEFAULT   15 global_int
    58: 0000000000003008     8 OBJECT  GLOBAL DEFAULT   15 global_int_ptr
```

So, as we can see, `global_int_ptr` is at an offset of `0x3008` and we know that
it is holding the address of `global_int` which is at an offset of `0x3000`. The
dynamic relocation corresponding to this is the first relocation listed above
(the one at offset `0x3008`, which is the offset of `global_int_ptr`.) According
to the ABI, `R_X86_64_RELATIVE` is to be applied as follows: At the load address
corresponding to the offset `0x3008`, store the load address corresponding to
the offset `0x3000`. This is exactly what we expect because we want
`global_int_ptr` to hold the address of `global_int` at run time.


