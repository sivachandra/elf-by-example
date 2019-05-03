## About

This repository is to serve as a way to learn and experiment with how compilers,
linkers, and the C runtime work cooperatively to make an application start, run, and
shutdown. Most of the concepts and the mechanics involved are explained using examples
from the `examples` directory of this git repository.

## Static Linking

Currently, we are limiting ourselves to static linking (both PIE and non-PIE variations).
At some point in future, we might add information and examples about dynamic linking.
In the meantime, interested readers can contribute dynamic linking related examples
and topics.

## Examples

Each example comes with its own `README.md` which explains what that example is trying
to illustrate. General information about the examples is available in `examples/README.md`.
It has information like suggested order of walking the examples, how to prepare a new
example, how to build an example etc.

## Prerequisites

This git repo has `musl-libc`, `glibc`, `gcc` and `llvm-project` as its submodules.
This makes the repo self contained with respect to the compilers, _libc_s and linkers
one needs for experimentation. But, it also means that one will have to do a one-time
build and setup of these compilers, _libc_s and linkers. There is a convenience
script, by name `build_prereq.py`, in the repo's root directory which can build and
set these up for use with experiments. Not suprisingly, `build_prereq.py` takes a
long time to finish as GCC and Clang are built from sources. Note also that
`build_prereq.py` does not install any dependencies required for building GCC and
Clang. One will have to install such dependencies separately. Conveniently though,
when `build_prereq.py` runs the configure step of say GCC, it will error out with
an indicative message if GCC's dependencies are missing.
