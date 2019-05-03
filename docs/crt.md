# The CRT

For a fully-statically linked PIE or non-PIE binary, the CRT is responsible for
three main tasks in order:
1. Application of startup relocations
2. Setup and initialization of TLS
3. Invoke initializers and finalizers

## Startup Relocations

In general, the CRT has to apply two types of relocations:
1. **Dynamic relocations** - In a static but non-pie binary, dynamic relocations
are not present. Such relocations are present in a static-pie linked binary
however. They typically adjust for the OS determined load address of the
executable. It is the responsibility of the CRT to apply dynamic relocations at
startup. Application of such relocations is explained in more detail in this
[example.](https://github.com/sivachandra/elf-by-example/tree/master/examples/global_var_ptr)
2. **ifunc relocations** - These type of relocations have to be applied to both 
static non-pie and static-pie binaries. To learn more about ifuncs and how ifunc
relocations are applied, see this [example.](https://github.com/sivachandra/elf-by-example/tree/master/examples/ifunc)

## Setup and Initialization of TLS

Right after applying the dynamic and ifunc relocations, the CRT has to
initialize the TLS for the main thread. The TLS layout depends on the thread
model adopted by the libc. Typically, libc implementations support the POSIX
pthreads based model and provide the stdlib threads.h API over it.
