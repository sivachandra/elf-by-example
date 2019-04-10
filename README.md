This is a convenience repository to do quick experiments with glibc and 
musl-libc.

To start experimenting, you will have to first setup the prerequisites. This
is done by running the script `build_prereq.py`. This builds and installs GCC,
glibc and musl-libc. Currently, this script does not install any prerequisites
required by GCC, glibc and musl-libc themselves. You will have to install them
separately. When run `build_prereq.py`, the configure steps for these
prerequisites will error out if their dependency is missing. The error message
will indicate what is missing and you can install it separately.

Building the prerequisites takes a long time as GCC is built and installed from
sources. It is expected that this step is a one time thing and hence this
long preparatory step is not going to be day-to-day pain.

Once the prerequisites are built and installed, one can start building the
examples against glibc and musl-libc using the script `build_example.py`. Run
the following to see more information on how to use it.

```shell
$> ./build_example.py --help
```

The `build_example.py` prints out the commands it is running. The resulting
binaries and object files end up in the `out` directory. One can then step
through them using GDB, or look at the `readelf` or `objdump` outputs to
learn about the different moving parts involved.
