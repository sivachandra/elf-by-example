`ifunc`s are _indirect_ functions. They are indirect because of the way they get
resolved at program startup time. For every `ifunc`, the libc CRT invokes the
corresponding  _resolver_ function. The resolver function return a pointer to
another function which has the same signature as its the indirect function. The
CRT then replaces the call sites to the `ifunc` with the return function
pointer. Hence, at runtime, calls to the `ifunc` actually invokes the function
returned by the resolver.

For `x86_64`, the information that there are `ifunc`s to resolve at startup, is
conveyed to the CRT by relocations of type `R_X86_64_IRELATIVE` in the section
named `rel.plt` or `rela.plt`.

When you build and run this example, you will notice that the executable linked
against musl-libc crashes. This is because, musl-libc's CRT does apply
`R_X86_64_IRELATIVE` relocations.
