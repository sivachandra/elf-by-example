#! /usr/bin/python -B

import argparse
import json
import os
import sys

import muslflex_utils


_COMPILERS = {
    "C": os.path.join(muslflex_utils.LLVM_BUILD_DIR, "bin", "clang"),
    "C++": os.path.join(muslflex_utils.LLVM_BUILD_DIR, "bin", "clang++"),
}

_LINKERS = [
    "ld",  # We will assume that the BFD linker is available in path as "ld".
    os.path.join(muslflex_utils.LLVM_BUILD_DIR, "bin", "ld.lld"),
]

_CONFIG_FILE = "CONFIG.json"
_CONFIG_OPTIONS = [
    "LANG",  # The language, either "C" or "C++". Other values are an error.
    "CCFLAGS",  # List of additional CCFLAGS for the compile step.
    "LDFLAGS",  # List of additional LDFLAGS for the link step.
]
_SUPPORTED_LANGUAGES = list(_COMPILERS.keys())
_LANG_SUFFIX = {
  "C": ".c",
  "C++": ".cc",
}


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


def _build(src_file, output_name, compiler, ccflags, ldflags):
  compiler_suffix = os.path.basename(compiler)
  for libc in ("glibc", "musl"):
    object_file = ".".join([output_name, compiler_suffix, libc, "o"])
    compile_cmd = [compiler,
                   "-nostdinc",
                   "-I" + _get_include_dir(libc),
                   "-I" + os.path.join(
                       muslflex_utils.GCC_INSTALL_DIR,
                       "lib/gcc/x86_64-pc-linux-gnu/9.0.1/include/"),
                   "-o", object_file, "-g", "-O0", "-c", src_file] + ccflags
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
                  "-o", exe_file] + ldflags
      muslflex_utils.run_step(name="Linking %s" % exe_file, cmd=link_cmd)


def _verify_config(config):
  for k in config.keys():
    if k not in _CONFIG_OPTIONS:
      sys.exit("Unknown CONFIG.json option '%s';\nAllowed options are %s" %
               (k, _CONFIG_OPTIONS))
    if k == "LANG":
      lang = config[k]
      if lang not in _SUPPORTED_LANGUAGES:
        sys.exit("Unsupported LANG value '%s' specified in CONFIG.json.\n"
                 "Supported values are %s" % (lang, _SUPPORTED_LANGUAGES))


def main():
  args = _parse_args()
  example_path = args.example
  if example_path.endswith("/"):
    example_path = example_path[:-1]
  basename = os.path.basename(example_path)
  example_build_dir = os.path.join(muslflex_utils.OUT_DIR, example_path)
  if not os.path.exists(example_build_dir):
    os.makedirs(example_build_dir)
  config_file = os.path.join(os.path.abspath(example_path), _CONFIG_FILE)
  ccflags = []
  ldflags = []
  if os.path.exists(config_file):
    with open(config_file, "r") as f:
      config = json.load(f)
    _verify_config(config)
    ccflags = config.get("CCFLAGS", [])
    if type(ccflags) is not list:
      sys.exit("CCFLAGS in %s should be a list." % config_file)
    ldflags = config.get("LDFLAGS", [])
    if type(ldflags) is not list:
      sys.exit("LDFLAGS in %s should be a list." % config_file)
  else:
    config = {"LANG": "C"}
  output_name = os.path.join(example_build_dir, basename)
  lang = config.get("LANG", "C")
  src_file = os.path.join(os.path.abspath(example_path),
                          "main%s" % _LANG_SUFFIX[lang])
  if not os.path.exists(src_file):
    exit("Did not find a main.c file in '%s'" % example_path)
  _build(src_file, output_name, _COMPILERS[lang], ccflags, ldflags)
  return 0
  

if __name__ == "__main__":
  main()
