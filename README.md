nano_lib_py
=======

Forked from https://github.com/Matoking/nanolib

Modifications : make it compatible with arm64 (macos m1/m2)


A set of tools for handling functions related to the NANO cryptocurrency protocol.

Features
========
* Solve and verify proof-of-work
* Create and deserialize legacy and universal blocks
* Account generation from seed using the same algorithm as the original NANO wallet and NanoVault
* Functions for converting between different NANO denominations
* High performance cryptographic operations using C extensions (signing and verifying blocks, and generating block proof-of-work)
  * Proof-of-work generation supports SSE2, SSSE3, SSE4.1, AVX and NEON instruction sets for improved performance. The best supported implementation is selected at runtime with a fallback implementation with universal compatibility.
* Backed by automated tests
* Compatible with Python 3.6 and up
* Licensed under the very permissive *Creative Commons Zero* license

Installation
============

You can install the library using pip:

```
pip install nano_lib_py
```

nano_lib_py requires a working build environment for the C extensions. For example, on Debian-based distros you can install the required Python header files and a C compiler using the following command:

```
apt install build-essential python3-dev
```

Documentation
=============

An online copy of the documentation can be found at [Read the Docs](https://nano_lib_py.readthedocs.io/en/latest/).

You can also build the documentation yourself by running `python setup.py build_sphinx`.

Commands
========

The `setup.py` script comes with a few additional commands besides installation:

* `build_sphinx`
  * Build the documentation in `build/sphinx/html`.
* `test`
  * Run tests using pytest
* `speed`
  * Run a benchmark testing the performance of various cryptographic operations used in the library.

Donations
=========

**xrb_33psgb1exxuftgjthbz4tsgzm5qmyzawrfzptpmp3nwzousbypqf6bcmrk69**
