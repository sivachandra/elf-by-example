## Components of a `libc`

The term **libc** is normally used to refer to a group of libraries and tools
constituting five different components:

1. **The C runtime, commonly referred to as the CRT** - This component is
responsible for the start-up and termination of an application.
2. **The C standard library** - This component provides the various C standard
libraries like math.h, stdio.h, thread.h etc.
3. **The POSIX extensions** - This component provides various POSIX extension
headers like `pthread.h`, `unistd.h` etc.
4. **Non-standard extensions** - These are extension utilities provided by a
typical modern libc. For example, `syscall.h`.
5. **The dynamic loader** - This component is responsible for dynamic loading
of shared libraries.

