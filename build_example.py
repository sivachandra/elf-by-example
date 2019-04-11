#! /usr/bin/python -B

import argparse
import os

import muslflex_utils


_COMPILERS = [
    os.path.join(muslflex_utils.LLVM_BUILD_DIR, "bin", "clang"),
    # Should we add GCC here?
]

_LINKERS = [
    "ld",  # We will assume that the BFD linker is available in path as "ld".
    os.path.join(muslflex_utils.LLVM_BUILD_DIR, "bin", "ld.lld"),
]

def _get_install_dir(libc):
  if libc == "glibc":
    return muslflex_utils.GLIBC_INSTALL_DIR
  elif libc == "musl":
    return muslflex_utils.MUSL_INSTALL_DIR
  else:
    assert False, "Unknown libc: %s" % libc


def _get_include_dir(libc):
  return os.path.join(_get_install_dir(libc), "include")


def _get_lib_dir(libc):
  return os.path.join(_get_install_dir(libc), "lib")


def _get_rcrt1(libc):
  return os.path.join(_get_lib_dir(libc), "rcrt1.o")


def _get_crti(libc):
  return os.path.join(_get_lib_dir(libc), "crti.o")


def _get_crtn(libc):
  return os.path.join(_get_lib_dir(libc), "crtn.o")


def _parse_args():
  parser = argparse.ArgumentParser(
      description="Script which can which can build an example in "
                  "various flavors")
  parser.add_argument(
      "--example", "-p", dest="example", type=str, required=True,
      help="Path to the example directory")
  return parser.parse_args()


def _build(src_file, output_name):
  for compiler in _COMPILERS:
    compiler_suffix = os.path.basename(compiler)
    for libc in ("glibc", "musl"):
      object_file = ".".join([output_name, compiler_suffix, libc, "o"])
      compile_cmd = [compiler,
                     "-nostdinc",
                     "-I" + _get_include_dir(libc),
                     "-I" + os.path.join(
                         muslflex_utils.GCC_INSTALL_DIR,
                         "lib/gcc/x86_64-pc-linux-gnu/9.0.1/include/"),
                     "-fPIC",
                     "-o", object_file, "-g", "-O0", "-c", src_file]
      muslflex_utils.run_step(name="Compiling %s" % object_file,
                              cmd=compile_cmd)
    
    for linker in _LINKERS:
      linker_suffix = os.path.basename(linker)
      for libc in ("glibc", "musl"):
        object_file = ".".join([output_name, compiler_suffix, libc, "o"])
        exe_file = object_file[:-1] + linker_suffix  # Remove .o and
                                                     # add .<linker name>
        link_cmd = [linker, "-nostdlib",
                    "-static",
                    "-pie", "--no-dynamic-linker",
                    "-L" + _get_lib_dir(libc),
                    "-L" + muslflex_utils.GCC_LIB_DIR,
                    object_file, _get_rcrt1(libc), _get_crti(libc),
                    muslflex_utils.GCC_CRT_BEGIN,
                    "--start-group", "-lc", "-lgcc", "-lgcc_eh", "--end-group",
                    muslflex_utils.GCC_CRT_END, _get_crtn(libc),
                    "-o", exe_file]
        muslflex_utils.run_step(name="Linking %s" % exe_file, cmd=link_cmd)


def main():
  args = _parse_args()
  example_path = args.example
  if example_path.endswith("/"):
    example_path = example_path[:-1]
  basename = os.path.basename(example_path)
  src_file = os.path.join(os.path.abspath(example_path), "main.c")
  output_name = os.path.join(muslflex_utils.OUT_DIR, example_path, basename)
  _build(src_file, output_name)
  return 0
  

if __name__ == "__main__":
  main()
