This is a convenience repository to do quick experiments to compare glibc and 
musl-libc.

To start experimenting, you will have to first setup the prerequisites. This
is done by running the script `build_prereq.py`. This builds and installs GCC,
glibc and musl-libc. Currently, this script does not install any prerequisites
required by GCC, glibc and musl-libc themselves. You will have to install them
separately.

Building the prerequisites takes a long time GCC is built and installed from
sources. It is expected that this step is a one time thing and hence this
long preparatory step is not going to be a pain to deal with.

Once the prerequisites are built and installed, one can start building the
examples against glibc and musl-libc using the script `build_example.py`. Run
the following to see more information on how to use it.

```shell
$> ./build_example.py --help
```
