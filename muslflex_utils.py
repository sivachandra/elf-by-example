import os
import subprocess
import sys

MUSLFLEX_SRC_ROOT = os.path.dirname(os.path.abspath(__file__))

GCC_SRC_ROOT = os.path.join(MUSLFLEX_SRC_ROOT, "gcc")
GCC_BUILD_DIR = os.path.join(MUSLFLEX_SRC_ROOT, "gcc-build")
GCC_INSTALL_DIR = os.path.join(MUSLFLEX_SRC_ROOT, "gcc-install")
GCC_LIB_DIR = os.path.join(GCC_INSTALL_DIR, "lib/gcc/x86_64-pc-linux-gnu/9.0.1")
GCC_CRT_BEGIN = os.path.join(GCC_LIB_DIR, "crtbeginS.o")
GCC_CRT_END = os.path.join(GCC_LIB_DIR, "crtendS.o")

GLIBC_SRC_ROOT = os.path.join(MUSLFLEX_SRC_ROOT, "glibc")
GLIBC_BUILD_DIR = os.path.join(MUSLFLEX_SRC_ROOT, "glibc-build")
GLIBC_INSTALL_DIR = os.path.join(MUSLFLEX_SRC_ROOT, "glibc-install")

MUSL_SRC_ROOT = os.path.join(MUSLFLEX_SRC_ROOT, "musl")
MUSL_INSTALL_DIR = os.path.join(MUSLFLEX_SRC_ROOT, "musl-install")

OUT_DIR = os.path.join(MUSLFLEX_SRC_ROOT, "out")


def run_step(name, cmd, cwd=None):
  process_options = {
      "stdout": subprocess.PIPE,
      "stderr": subprocess.STDOUT,
  }
  if cwd:
    process_options["cwd"] = cwd
  print(">>> STEP: %s" % name)
  print("    COMMAND: %s" % cmd)
  print("    CWD: %s" % cwd)
  process = subprocess.Popen(cmd, **process_options)
  stdout, _ = process.communicate()
  if process.returncode != 0:
    sys.exit("!!! FAILED !!!\n%s" % stdout)
