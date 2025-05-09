ZParser2 Cli Argument Parsing Library


`zparser2` is probably the simplest most opinionated argument parsing library. Lot's of conventions, zero configuration!

If you add the `@z.task` notation to a function, it automatically become available to the CLI.
The function's parameters are what the CLI will expect. If notations are given, type will be enforced.
The file in which the function is located will be the module in which the function will be available.

The downside is that you can only have two layers in your cli. That being said, more than that would be too complex and less than that you don't really need a library.


Example
-------

Let's say you have 3 files:


math_functions.py
```
"""here we do math"""
from zparser2 import z

@z.task
def duplicate_number(x: float):
    """returns twice the value of x"""
    return 2*x

@z.task
def triple_number(x: float):
    """returns 3 times the value of x"""
    return 3*x
```

string_functions.py
```
"""string processing"""
from zparser2 import z

@z.task
def add_square_brackets_to_string(x: str):
    """x -> [x]"""
    return f"[{x}]"

@z.task
def first_word(x: str):
    """returns the first word of a string"""
    return x.split(" ")[0]

@z.task
def last_word(x: str):
    """returns the first word of a string"""
    return x.split(" ")[-1]

@z.task
def another_task(somestring: str, some_int: int, workdir=None, root_url=None):
    """description of the task"""
    print(f"somestring={somestring}")
    print(f"some_int={some_int}")
    print(f"workdir={workdir}")
    print(f"root_url={root_url}")
```


mycli.py
```
#!/usr/bin/env python3
import zparser2

import math_functions
import string_functions

if __name__ == "__main__":
    zparser2.init()
```

Output
------

```
(env2) mdiez@batman:~/code/zparser2/example$ ./mycli.py
./mycli.py <plugin_name> <task>
Plugin list:
  math_functions       - here we do math
  string_functions     - string processing

```

```
(env2) mdiez@batman:~/code/zparser2/example$ ./mycli.py string_functions
You need to specify a task
--------------------------------------------------------------------------------
string processing
./mycli.py string_functions <task>
Plugin alias: []
Tasks:
  add_square_brackets_to_string - x -> [x]
  another_task         - description of the task
  first_word           - returns the first word of a string
  last_word            - returns the first word of a string
```

```
(env2) mdiez@batman:~/code/zparser2/example$ ./mycli.py string_functions another_task
You need to specify the required arguments [somestring, some_int]
--------------------------------------------------------------------------------
description of the task
Usage:
  ./mycli.py string_functions another_task somestring some_int [--workdir workdir] [--root_url root_url]
Positional arguments:
  somestring -  <class 'str'>
  some_int -  <class 'int'>
Optional arguments:
  --workdir (Default: None)  -
  --root_url (Default: None)  -
```

```
(env2) mdiez@batman:~/code/zparser2/example$ ./mycli.py string_functions another_task blah 42 --root_url https://blah.com
somestring=blah
some_int=42
workdir=None
root_url=https://blah.com
```


How to build & publish
----------------------

* `python3 -m build`
* `python3 -m twine upload --repository testpypi dist/*`

