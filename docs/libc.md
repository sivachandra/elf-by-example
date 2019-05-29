## Components of a `libc`

A modern, standards compliant **libc** implementation consists of the following
libraries, tools and sub-systems.

1. **The C runtime, commonly referred to as the CRT** - This component is
responsible for the start-up and termination of an application. More information
about the CRT can be found [here](crt.md).
2. **The C standard library** - This component provides the various C standard
libraries like math.h, stdio.h, thread.h etc.
3. **The POSIX extensions** - This component provides various POSIX extension
headers like `pthread.h`, `unistd.h` etc.
4. **Library files** - Most of libc is made available as `libc.a` or `libc.so`.
However, for POSIX compliance, few parts of the libc implementation are grouped
into their own `.a` or `.so` files. For example, POSIX requires that the math
functions be packaged as a `libm.a` for static linking and `libm.so` for dynamic
linking. Hence, though the C standard does not require such a packaging scheme,
all POSIX compliant libc implementations provide `libm.a` and `libm.so` separate
from `libc.a` and `libc.so`. Same is true with `pthread` and a bunch of other
library files as well. Though they are packaged into separate library files,
they are all considered as part of a, and provided by, a single libc
implementation.
5. **Non-standard extensions** - These are extension utilities provided by a
typical modern libc. For example, `syscall.h`.
6. **The dynamic loader** - This component is responsible for dynamic loading
of shared libraries.
