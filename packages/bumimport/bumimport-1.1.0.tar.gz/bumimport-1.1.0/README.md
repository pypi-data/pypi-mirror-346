# bumimport
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)

So you're about to append to `sys.path` in order to import something when a `Neckbeard` on Stack Overflow tells you it's "bad practice"...

Well, the `Neckbeard` is right, and you probably should learn how to use the import system properly. However, if you insist on being a `Bum`, here's a safer alternative.

----
You might be tempted to append to `sys.path` so that you can import a module from another directory like importing `module1` in `main.py` in the example below.

```bash
├── main.py
├── bucket_o_modules/
│   ├── module1.py
│   ├── module2.py
```

Of course, you can just add `__init__.py` to `bucket_o_modules/` so that you can import `module1` from `bucket_o_modules` in `main.py`.

```bash
├── main.py
├── bucket_o_modules/
│   ├── __init__.py
│   ├── module1.py
│   ├── module2.py
```

However, this only works when `main.py` and `bucket_o_modules/` are in the same package. Not to mention, a more complicated file structure would require you to add `__init__.py` to every subdirectory.

```bash
├── main.py
├── bucket_o_modules/
│   ├── __init__.py
│   ├── module1.py
│   ├── extra_special_modules/
│   │   ├── __init__.py
│   │   ├── module2.py
```

This has its own downsides. `module1` and `module2` now have to be imported from different packages, `bucket_o_modules` and `bucket_o_modules.extra_special_modules`, respectively. You can get arround this by adding code within each `__init__.py` to "pull up" each of the modules into each package's parent package, but by now you can probably see this is getting tedious, and it would be annoying to maintain as the contents of `bucket_o_modules/` change.

----
This is where `bumimport` comes into play.

Instead of using the following code to import any module from `bucket_o_modules/`:

```python
import importlib
import sys

sys.path.append("/path/to/bucket_o_modules/")

mod = importlib.import_module("module1")
```

Use the following:

```python
import sys

import bumimport

bumimport.flat_import(__name__, "/path/to/bucket_o_modules/")

mod = getattr(sys.modules[__name__], "module1")
```

`flat_import` adds all the modules within `bucket_o_modules/` to the module `__name__` (the current module) as attributes. Those attributes can then be accessed with `getattr()`.

Likewise, instead of using the following code to import any module from `bucket_o_modules/` or any of its subdirectories:

```python
import importlib
import os
import sys

for root, _, _ in os.walk("/path/to/bucket_o_modules/"):
    sys.path.append(root)

mod = importlib.import_module("module1")
```

Use the exact same code as before:

```python
import sys

import bumimport

bumimport.flat_import(__name__, "/path/to/bucket_o_modules/")

mod = getattr(sys.modules[__name__], "module1")
```

`bumimport` really thrives when you use it in a single `__init__.py` in the root of a package. Consider the following file structure:

```bash
├── main.py
├── bucket_o_modules/
│   ├── __init__.py
│   ├── module1.py
│   ├── extra_special_modules/
│   │   ├── module2.py
```

If `__init__.py` contains the following:

```python
from bumimport import flat_import as _flat_import

_flat_import(__name__, __file__)
```

Then the following code can be used in `main.py`:

```python
import bucket_o_modules

mod1 = getattr(bucket_o_modules, "module1")
mod2 = getattr(bucket_o_modules, "module2")
```

Now you can access the modules in `bucket_o_modules/` as if it was a flattened package. Additionally, modules with invalid names like `os`, `mod.ule1`, or `mod-ule1` can still be accessed (`getattr()` required for any name that breaks dot notation).

----
`bumimport` is safer because it never modifies `sys.path` which means there is no risk of modules getting masked. It also prevents any module with the same name as an existing attribute from being added which means there's no confusion over which module you end up having access to. Lastly, the imported modules are never added to `sys.modules` which means there will never be conflicts with the standard library.

## Installation
- With pip:

        pip install bumimport
