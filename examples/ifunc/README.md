# Understanding `ifunc` Relocations

`ifuncs` are _indirect_ functions. They are indirect because of the way they get
resolved at program startup time. For every `ifunc`, the libc CRT invokes a
corresponding  _resolver_ function. This resolver function returns a pointer to
another function which has the same signature as the `ifunc`. The CRT then
replaces the call sites to the `ifunc` with calls to the function returned by
the resolver. Hence, at runtime, calls to the `ifunc` actually invokes the
function returned by the resolver.

For `x86_64`, the information that there are `ifuncs` to resolve at startup, is
conveyed to the CRT by relocations of type `R_X86_64_IRELATIVE` in the sections
named `.rel.plt` or `.rela.plt`. The reason why we have the `.plt` suffix is
explained below.

When you build and run this example, you will notice that the executable linked
against musl-libc crashes. This is because, musl-libc's CRT does apply
`R_X86_64_IRELATIVE` relocations. That is, it does not invoke the resolver
functions at startup time. But, for the purpose of further discussion, we
will use the musl-linked binaries as they are easier to analyze with `readelf`.

Let take look at the relevant part of the readelf output for the binary
`out/examples/ifunc/ifunc.clang.musl.ld.lld`:

```
Relocation section '.rela.plt' at offset 0x290 contains 1 entry:
    Offset             Info             Type               Symbol's Value  Symbol's Name + Addend
0000000000003030  0000000000000025 R_X86_64_IRELATIVE                        1010
```

For the same binary, the section-headers part of the readelf dump shows this:

```
[Nr] Name              Type            Address          Off    Size   ES Flg Lk Inf Al
...
[19] .got.plt          PROGBITS        0000000000003018 003018 000020 00  WA  0   0  8
```

Notice that the offset at which the `R_X86_64_IRELATIVE` relocation is to be
applied falls in the `.got.plt` section and not the `.text` section. This is
because, text relocations are not allowed at run time, so the linker generates
a PLT based relocation. This is the reason why the `ifunc` related relocations
are listed in `.rel[a].plt` (with the `.plt` prefix indicating that it
corresponds to relocations for entities listed in the PLT).
