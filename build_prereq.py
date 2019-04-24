#! /usr/bin/python

import argparse
import os
import shutil
import sys

import muslflex_utils


def _parse_args():
  parser = argparse.ArgumentParser(description="Build muslflex prerequisites.")
  parser.add_argument("--clean", "-x", dest="clean", action="store_true",
                      help="Perform a clean build.")
  parser.add_argument("--component", "-r", dest="component", default=None,
      help="The component to build. All components will be built by default.")
  return parser.parse_args()


def _build_musl(options):
  configure_script = os.path.join(muslflex_utils.MUSL_SRC_ROOT, "configure")
  configure_options = ["CFLAGS=%s" % "-g -O0",
                       "--disable-shared",
                       "--prefix=%s" % muslflex_utils.MUSL_INSTALL_DIR]
  if options.clean:
    muslflex_utils.run_step(name="Cleaning previous muls-libc build",
                             cmd=['make', 'clean'],
                             cwd=muslflex_utils.MUSL_SRC_ROOT)
  muslflex_utils.run_step(name="Configuring musl-libc",
                          cmd=[configure_script] + configure_options,
                          cwd=muslflex_utils.MUSL_SRC_ROOT)
  muslflex_utils.run_step(name="Building musl-libc",
                          cmd=["make", "-j16"],
                          cwd=muslflex_utils.MUSL_SRC_ROOT)
  muslflex_utils.run_step(name="Installing musl-libc",
                          cmd=["make", "install"],
                          cwd=muslflex_utils.MUSL_SRC_ROOT)


def _build_glibc(options):
  configure_script = os.path.join(muslflex_utils.GLIBC_SRC_ROOT, "configure")
  # TODO(sivachandra): Make a debug build if options say so.
  configure_options = ["--enable-static-pie",
                       "--prefix=%s" % muslflex_utils.GLIBC_INSTALL_DIR]
  muslflex_utils.run_step(name="Configuring glibc",
                          cmd=[configure_script] + configure_options,
                          cwd=muslflex_utils.GLIBC_BUILD_DIR)
  muslflex_utils.run_step(name="Building glibc",
                          cmd=["make", "-j16"],
                          cwd=muslflex_utils.GLIBC_BUILD_DIR)
  muslflex_utils.run_step(name="Installing glibc",
                          cmd=["make", "install"],
                          cwd=muslflex_utils.GLIBC_BUILD_DIR)


def _build_gcc(options):
  configure_script = os.path.join(muslflex_utils.GCC_SRC_ROOT, "configure")
  configure_options = ["--prefix=%s" % muslflex_utils.GCC_INSTALL_DIR,
                       "--enable-languages=c,c++",
                       "--disable-multilib"]
  muslflex_utils.run_step(name="Configuring GCC",
                          cmd=[configure_script] + configure_options,
                          cwd=muslflex_utils.GCC_BUILD_DIR)
  muslflex_utils.run_step(name="Building GCC",
                          cmd=["make", "-j16"],
                          cwd=muslflex_utils.GCC_BUILD_DIR)
  muslflex_utils.run_step(name="Installing GCC",
                          cmd=["make", "install"],
                          cwd=muslflex_utils.GCC_BUILD_DIR)


def _build_llvm(options):
  if options.clean:
    shutil.rmtree(muslflex_utils.LLVM_BUILD_DIR)
  if not os.path.exists(muslflex_utils.LLVM_BUILD_DIR):
    os.mkdir(muslflex_utils.LLVM_BUILD_DIR)
  muslflex_utils.run_step(
      name="Running LLVM CMake",
      cmd=["cmake", muslflex_utils.LLVM_DIR, "-DCMAKE_BUILD_TYPE=Debug",
           "-DLLVM_ENABLE_PROJECTS=llvm;clang;lld", "-G","Ninja"],
      cwd=muslflex_utils.LLVM_BUILD_DIR)
  muslflex_utils.run_step(
      name="Running Ninja to build LLVM",
      cmd=["ninja"],
      cwd=muslflex_utils.LLVM_BUILD_DIR)


_BUILDERS = {
    "musl": _build_musl,
    "glibc": _build_glibc,
    "gcc": _build_gcc,  # We need a gcc build because of crtBegin*
    "llvm": _build_llvm,
}


def main():
  args = _parse_args()
  if args.component is not None:
    builder = _BUILDERS.get(args.component)
    if not builder:
      sys.exit("ERROR: Unknown component '%s'." % args.component)
    _BUILDERS[args.component](args)
  else:
    for component, builder in _BUILDERS.items():
      builder(args)
  return 0


if __name__ == "__main__":
  main()
