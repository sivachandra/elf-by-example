#! /usr/bin/python

import argparse
import os

import muslflex_utils


def _parse_args():
  parser = argparse.ArgumentParser(description="Build muslflex prerequisites.")
  parser.add_argument("--debug", "-g", dest="debug", action="store_true",
                      help="Make debug builds of all prerequisities.")
  return parser.parse_args()


def _build_musl(options):
  configure_script = os.path.join(muslflex_utils.MUSL_SRC_ROOT, "configure")
  cflags = ["-fPIC"]
  if options.debug:
    cflags.append("-g")
  configure_options = ["CFLAGS=%s" % " ".join(cflags),
                       "--disable-shared",
                       "--prefix=%s" % muslflex_utils.MUSL_INSTALL_DIR]
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


def _run_cmake():
  muslflex_utils.run_step(
      name="Running cmake",
      cmd=["cmake", muslflex_utils.MUSLFLEX_SRC_ROOT],
      cwd=muslflex_utils.OUT_DIR)


def main():
  args = _parse_args()
  _build_musl(args)
  _build_glibc(args)
  _build_gcc(args)
  _run_cmake()
  return 0


if __name__ == "__main__":
  main()
