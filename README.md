EasyEuler
=========
EasyEuler is a configurable command line tool for working with Project Euler.
It provides support for many languages out of the box and adding more is easy.

This project was inspired by [EulerPy](https://github.com/iKevinY/EulerPy)
and intends to provide the same functionality for a larger variety of languages.


Installation
============
EasyEuler can be installed from PyPI using [pip](https://pip.pypa.io/en/latest/):
```bash
$ pip install easyeuler
```


Usage
=====
Use `create` to create a new problem file:
```bash
$ easyeuler create 1 python
Written to euler_001.py

$ cat euler_001.py
"""
Problem 1: Multiples of 3 and 5

If we list all the natural numbers below 10 that are multiples of 3 or 5,
we get 3, 5, 6 and 9. The sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.

"""
```

Once you've come up with a solution, output the result and check if it's
correct with `verify`:
```bash
$ easyeuler verify euler_001.py
Checking output of euler_001.py: [no output]  # output in red

$ echo print(12345) > euler_001.py
$ easyeuler verify euler_001.py
Checking output of euler_001.py: 12345        # incorrect solution, output in red

$ echo print(42) > euler_001.py
$ easyeuler verify euler_001.py
Checking output of euler_001.py: 42           # correct solution, output in green
```

You can even time the execution of your solutions with the `time` flag:
```bash
$ easyeuler verify --time euler_001.py
Checking output of euler_001.py: 42
CPU times - user: 16.7ms, system: 3.33ms, total: 20ms
Wall time: 1.02s
```

...and execute multiple at once:
```bash
$ easyeuler verify *
Checking output of euler_001.py: 42
Checking output of euler_002.c: 12345
Checking output of euler_003.py: [error]  # [error] is displayed if an error occurs during execution
```

Some problems come with additional files, use `generate-resources` to generate
those:
```bash
$ easyeuler create 22 python
Written to euler_022.py
$ cat euler_022.py
"""
Problem 22: Names scores

[....]

This problem references the following resources:

names.txt

"""

$ easyeuler generate-resources 22  # specify the problem ID to generate problem-specific resources
Created names.txt at path .

$ easyeuler generate-resources     # or leave it empty to generate all resources
[....]
Created 326_formula2.gif at path .
Created 326_formula1.gif at path .
Created 327_rooms_of_doom.gif at path .
Created 330_formula.gif at path .
```

Use `list` and `show` to browse problems:
```bash
$ easyeuler list
Problem 1: Multiples of 3 and 5
Problem 2: Even Fibonacci numbers
Problem 3: Largest prime factor
Problem 4: Largest palindrome product
Problem 5: Smallest multiple
[....]

$ easyeuler show 2
Problem 2: Even Fibonacci numbers

Each new term in the Fibonacci sequence is generated by adding the
previous two terms. By starting with 1 and 2, the first 10 terms will be:

                  1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...

Find the sum of all the even-valued terms in the sequence which do not
exceed four million.
```


Configuration
=============
EasyEuler is designed to be configurable and adaptable to any language
you may want to use it with.
Adding a new language is as easy as adding a few lines to the `config.json` file (located in `EasyEuler/`).

A language has the following attributes:

- `name` - the name of the language.
- `extension` - the file extension of the language.
- `command` - the command to execute with the `verify` command.
- `template` - the name of the template (located in `EasyEuler/templates/`)

Templates use the [Jinja2](http://jinja.pocoo.org) templating engine.


Requirements
============
EasyEuler requires [Python 3.5+](https://www.python.org/downloads/release/python-350/),
along with the [Click](http://click.pocoo.org) and [Jinja2](http://jinja.pocoo.org) modules.


Acknowledgements
================
The problem descriptions are courtesy of the
[EulerPy](https://github.com/iKevinY/EulerPy) project,
which formatted the descriptions from Kyle Keen's
[Local Euler](http://kmkeen.com/local-euler) project into a human-readable form.


License
=======
EasyEuler is licensed under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
