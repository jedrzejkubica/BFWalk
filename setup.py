# compiles code in the BFWalk-C submodule into a shared library
# installed inside the bfwalk package as bfwalk/_libbfwalk*.so,
# all other package settings are in pyproject.toml
#
# library is loaded with ctypes (see BFWalk/bfwalk.py), it is not a real
# python extension module: we use setuptools to compile it

import glob
import os
import subprocess
import sys

from setuptools import Extension, setup

C_DIR = "BFWalk-C"

# Same rule as BFWalk-C/Makefile: compile every .c file that has a matching .h
# (but skip testAdjacency.c, which contains a main())
c_sources = []
for c_file in sorted(glob.glob(C_DIR + "/*.c")):
    h_file = c_file[:-2] + ".h"
    if os.path.exists(h_file):
        c_sources.append(c_file)

if len(c_sources) == 0:
    raise SystemExit("ERROR: no C source files found in " + C_DIR + "/, " +
                     "you probably need to run: git submodule update --init")

if sys.platform == "darwin":
    # Apple's clang has no built-in OpenMP, use libomp from Homebrew (brew install libomp)
    try:
        libomp = subprocess.check_output(["brew", "--prefix", "libomp"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        raise SystemExit("ERROR: on macOS BFWalk needs OpenMP, please run: brew install libomp")
    openmp_compile_args = ["-Xpreprocessor", "-fopenmp", "-I" + libomp + "/include"]
    openmp_link_args = ["-L" + libomp + "/lib", "-lomp"]
else:
    openmp_compile_args = ["-fopenmp"]
    openmp_link_args = ["-fopenmp"]

bfwalk_c = Extension(
    name="BFWalk._libbfwalk",
    sources=c_sources,
    # same flags as in BFWalk-C/Makefile
    extra_compile_args=["-std=c17", "-O2", "-fvisibility=hidden"] + openmp_compile_args,
    extra_link_args=openmp_link_args,
    libraries=["z", "m"],
    # python adds -DNDEBUG by default, but we want to keep the C asserts like the Makefile does
    undef_macros=["NDEBUG"],
)

setup(ext_modules=[bfwalk_c])
