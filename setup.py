#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import glob
import io
import os
import platform
from distutils.ccompiler import get_default_compiler

from setuptools import Extension, setup

# Package meta-data.
NAME = 'nano_lib_py'
DESCRIPTION = \
    'Forked Python library for working with the NANO cryptocurrency protocol'
URL = 'https://github.com/gr0vity-dev/nano-lib-py'
EMAIL = 'jannepulk@gmail.com'
AUTHOR = 'Janne Pulkkinen'
REQUIRES_PYTHON = '>=3.6.0'

# What packages are required for this module to be executed?
REQUIRED = [
    'py-ed25519-blake2b>=0.1.0',
    'py-cpuinfo>=4'
]


def get_compile_args(iset=None, build_platform="x86"):
    flags = {
        "unix": {
            "avx": ["-DWORK_AVX", "-mavx"],
            "sse4_1": ["-DWORK_SSE4_1", "-msse4.1"],
            "ssse3": ["-DWORK_SSSE3", "-mssse3"],
            "sse2": ["-DWORK_SSE2", "-msse2"],
            "neon": ["-DWORK_NEON"],
            None: ["-DWORK_REF"]
        },
        "msvc": {
            "avx": ["/DWORK_AVX", "/arch:AVX", "/DHAVE_AVX", "/D__SSE4_1__"],
            "sse4_1": ["/DWORK_SSE4_1", "/arch:SSE2", "/D__SSE4_1__"],
            "ssse3": ["/DWORK_SSSE3", "/arch:SSE2", "/D__SSSE3__"],
            "sse2": ["/DWORK_SSE2", "/arch:SSE2", "/D__SSE2__"],
            "neon": ["/DWORK_NEON"],
            None: ["/DWORK_REF"]
        }
    }

    # "-mfpu=neon" is only required when building on Linux & 32-bit ARM;
    # it is required on 64-bit ARM and is thus not recognized
    if build_platform == "arm":
        flags["unix"]["neon"].append("-mfpu=neon")

    compiler = get_default_compiler()

    try:
        return flags[compiler][iset]
    except KeyError:
        raise OSError("Compiler '{}' not supported.".format(compiler))


SOURCE_ROOT = os.path.join("src", "nano_lib_py-work-module", "BLAKE2")
SOURCE_FILES = {
    "ref": glob.glob(os.path.join(SOURCE_ROOT, "ref", "blake2b*.c")),
    "sse": glob.glob(os.path.join(SOURCE_ROOT, "sse", "blake2b*.c")),
    "neon": glob.glob(os.path.join(SOURCE_ROOT, "neon", "blake2b-*.c"))
}


def create_work_extension(source_name="ref", iset=None, build_platform=None):
    source_path = os.path.join(
        "src", "nano_lib_py-work-module", "BLAKE2", source_name
    )
    module_suffix = iset if iset else "ref"

    return Extension(
        "nano_lib_py._work_{}".format(module_suffix),
        include_dirs=[source_path],
        sources=[
            os.path.join("src", "nano_lib_py-work-module", "work.c")
        ] + SOURCE_FILES[source_name],
        extra_compile_args=get_compile_args(iset, build_platform)
    )


EXTENSIONS_TO_BUILD = []

_machine = platform.machine()

_is_unix_compiler = get_default_compiler() == "unix"

# https://stackoverflow.com/a/45125525
_is_arm = _machine.startswith("arm")
_is_arm64 = _machine.startswith("arm64")  # macos m2
_is_aarch64 = _machine.startswith("aarch64")
# 'AMD64' only appears on Windows
_is_x86 = _machine.startswith("x86") or _machine in ("i386", "i686", "AMD64")


if _is_x86:
    EXTENSIONS_TO_BUILD = [
        create_work_extension("sse", "avx", "x86"),
        create_work_extension("sse", "sse4_1", "x86"),
        create_work_extension("sse", "ssse3", "x86"),
        create_work_extension("sse", "sse2", "x86"),
        create_work_extension("ref", None, "x86")
    ]
elif _is_arm64:
    EXTENSIONS_TO_BUILD = [
        create_work_extension("ref", None, "arm")
    ]
elif _is_arm:
    EXTENSIONS_TO_BUILD = [
        create_work_extension("neon", "neon", "arm"),
        create_work_extension("ref", None, "arm")
    ]
elif _is_aarch64:
    EXTENSIONS_TO_BUILD = [
        create_work_extension("neon", "neon", "aarch64"),
        create_work_extension("ref", None, "aarch64")
    ]
else:
    EXTENSIONS_TO_BUILD = [create_work_extension("ref")]

EXTENSIONS_TO_BUILD.append(
    Extension(
        "nano_lib_py._nbase32",
        include_dirs=[os.path.join("src", "nano_lib_py-nbase32-module")],
        sources=[
            os.path.join("src", "nano_lib_py-nbase32-module", "nbase32.c"),
            os.path.join("src", "nano_lib_py-nbase32-module", "bit_array.c")
        ],
        # Older GCC versions require that we specify the C spec explicitly
        extra_compile_args=["-std=c99"] if _is_unix_compiler else None
    )
)

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!


# Where the magic happens:
setup(
    name=NAME,
    version='0.5.4',
    description=DESCRIPTION,
    # long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    ext_modules=EXTENSIONS_TO_BUILD,
    packages=["nano_lib_py"],
    package_data={"": ["LICENSE"]},
    package_dir={"nano_lib_py": "src/nano_lib_py"},
    install_requires=REQUIRED,
    # setup_requires=["sphinx"],
    include_package_data=True,
    license='CC0',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        #  'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Topic :: Office/Business :: Financial',
    ]
)
