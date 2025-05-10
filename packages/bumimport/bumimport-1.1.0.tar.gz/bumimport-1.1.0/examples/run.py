"""Demonstrate the flat_import strategy"""

import os
import sys

_DIR = os.path.dirname(os.path.realpath(__file__))
_DIR = os.path.normpath(os.path.join(_DIR, ".."))

sys.path.insert(0, _DIR)

import package  # noqa: E402

mod1 = getattr(package, "module1")
mod1.func1()

mod2 = getattr(package, "module2")
mod2.func2()
