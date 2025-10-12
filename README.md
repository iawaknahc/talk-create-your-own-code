# Disallow a specific code pattern in Python

Recent efforts such as mypy (PEP 484) and LSP implementation like Pyright brings static type checking to Python.
Type checking does help eliminating some kinds of programming errors, however,
it is not a silver bullet.
Other techniques like linting and testing complement type checking to make your codebase more robust.
This writing discusses how can we create new laws to govern our codebase.

Python is known for having a rich standard library.
One very common programming task is to process a URL.
Typically you need to parse the URL, extract the information from it, change one or two query parameters, and finally compose it into a new URL.
In Python, `urllib.parse` is the obvious choice for this task.

If you take a closer look into `urllib.parse`, you will see there exist two very similar pairs of functions, namely `url[un]parse` and `url[un]split`.
The difference is that `url[un]parse` implements RFC1808 while `url[un]split` implements RFC3986.
RFC1808 was obsoleted by RFC3986.
One noticeable difference is the removal of `;parameters` in RFC 3986.
An example is the best way to explain this.

```
>>> import urllib.parse
>>> urllib.parse.urlparse("/path;params")
ParseResult(scheme='', netloc='', path='/path', params='params', query='', fragment='')
>>> urllib.parse.urlsplit("/path;params")
SplitResult(scheme='', netloc='', path='/path;params', query='', fragment='')
```

So you will get an incorrect path if:

- The input path contains a `;`.
- You use `urlparse` (the one superseded by `urlsplit`) to parse the URL.

Type checking cannot prevent this kind of problem.
Testing might prevent it if your test suite covers an input with a `;`.
A custom lint rule can prevent it if you have the prior knowledge of `url[un]parse` should not be used in 2025 and onwards.

Once you have identified a certain code pattern should never exist in your codebase,
your next step is to codify it into a code (law) that can be enforced on everyone working on the codebase.
In Python, you can do this with Pylint custom checkers.
The technical details are not very interesting to be discussed here.
This repository contains an implementation of a checker that can be configured to forbid `url[un]parse`.
You may also find [How to Write a Checker](https://pylint.readthedocs.io/en/stable/development_guide/how_tos/custom_checkers.html) a useful reference.
Here is how the output looks like

```
$ make pylint
PYTHONPATH="$PWD/pylint_checkers" pylint test.py
************* Module test
test.py:2:0: E9601: urllib.parse.urlparse is restricted (restricted-module-items)
test.py:2:0: E9601: urllib.parse.urlunparse is restricted (restricted-module-items)
test.py:11:8: E9601: urllib.parse.urlparse is restricted (restricted-module-items)
test.py:12:8: E9601: urllib.parse.urlunparse is restricted (restricted-module-items)

------------------------------------------------------------------
Your code has been rated at 0.00/10 (previous run: 0.00/10, +0.00)

make: *** [Makefile:7: pylint] Error 2
```
