"""Implementations of import strategies"""

import importlib.util
import os
from pathlib import Path
import re
import sys
from types import ModuleType


def flat_import(
    module: str | ModuleType, path: str | Path, ignore: str | re.Pattern[str] = "__init__"
) -> None:
    """Recursively import all modules in a path to the provided module"""

    if isinstance(module, str):
        if module in sys.modules:
            module = sys.modules[module]
        else:
            raise ValueError(f"No module named: {module}")
    elif not isinstance(module, ModuleType):
        raise TypeError(f"Invalid module type: {type(module)}")

    if isinstance(path, str):
        if os.path.isfile(path):
            path = os.path.dirname(path)  # call flat_import with path=__file__
        elif not os.path.isdir(path):
            raise ValueError(f"No path named: {path}")
    elif not isinstance(path, Path):
        raise TypeError(f"Invalid path type: {type(path)}")

    if isinstance(ignore, str):
        ignore = re.compile(ignore)
    elif not isinstance(ignore, re.Pattern):
        raise TypeError(f"Invalid ignore type: {type(ignore)}")

    for root, _, files in os.walk(path):
        for f in files:
            f_root, f_ext = os.path.splitext(f)
            if f_ext == ".py" and not ignore.match(f_root):
                if hasattr(module, f_root):
                    raise ImportError(f"Multiple modules named: {f_root}")
                spec = importlib.util.spec_from_file_location(f_root, os.path.join(root, f))
                if spec is None:
                    raise ImportError(f"File cannot be imported: {os.path.join(root, f)}")
                mod = importlib.util.module_from_spec(spec)
                if spec.loader is None:
                    raise ImportError(f"Spec has no loader: {f_root}")
                spec.loader.exec_module(mod)
                setattr(module, f_root, mod)
