# Disallow the use of some specific module items in Python

## Static typing checking is not a silver bullet

mypy (PEP 484) and LSP servers like Pyright brings static type checking to Python.
Static type checking does help preventing some kinds of programming errors,
like accessing an undefined property in a class.
However, it does not help when we want to add additional law in addition to the rules imposed by the type checkers.

## Case study 1: `urllib.parse` from the standard library

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

## Case Study 2: `celery.group`

Celery is one of the most widely used task queue framework in Python.
It is feature-rich, and if used without care,
some advanced features may become footgun.

`celery.group` is a feature to allow you to execute several tasks in parallel,
and get the results when they are all done.
This feature is handy when your task is purely computational
and you want to leverage the number of CPUs to speed it up.

However, if the task is not computational,
but a request to an LLM that could spend a lot of credits,
then `celery.group` is not a good abstraction for you.
For example, the result of `celery.group` is not persisted,
if you retry the task, credits are spent again,
and you may suffer a great financial loss.

## Introduce your own law with Pylint custom checker

From the above case studies,
we can see that the potentially problematic code can be detected
with some static analysis.
For example, we can prevent the problem in case study 1
if we can forbid the use of `urllib.parse.url[un]parse`,
and we can prevent potent misuse of `celery.group` by
aggressively banning `celery.group`.

If you come from the JavaScript ecosystem and have experience with ESLint,
then what we want is the equivalent of [no-restricted-imports](https://eslint.org/docs/latest/rules/no-restricted-imports) in Python.
Unfortunately Pylint does not support no-restricted-imports out-of-the-box.
The good news is that it is not difficult to roll your own custom Pylint checker.

The technical details of writing a custom checker is not very interesting to be discussed here.
This repository contains a minimal implementation of no-restricted-imports.
Here are 2 pieces of information that can definitely help you with writing a custom checker

1. [How to write a checker](https://pylint.readthedocs.io/en/stable/development_guide/how_tos/custom_checkers.html)
2. [Documentation on Astroid Nodes](https://pylint.readthedocs.io/projects/astroid/en/stable/api/astroid.nodes.html)

The output of the custom checker looks like this

```
PYTHONPATH="$PWD/pylint_checkers" pylint test.py
************* Module test
test.py:2:0: E9601: urllib.parse.urlparse is restricted (restricted-module-items)
test.py:2:0: E9601: urllib.parse.urlunparse is restricted (restricted-module-items)
test.py:5:0: E9601: celery.group is restricted (restricted-module-items)
test.py:14:8: E9601: urllib.parse.urlparse is restricted (restricted-module-items)
test.py:15:8: E9601: urllib.parse.urlunparse is restricted (restricted-module-items)
test.py:19:20: E9601: celery.group is restricted (restricted-module-items)

------------------------------------------------------------------
Your code has been rated at 0.00/10 (previous run: 0.00/10, +0.00)

make: *** [Makefile:7: pylint] Error 2
```

So a PR with changes involving the use of restricted module items cannot build successfully in your CI pipeline.
The author of the PR is then forced to look up the reason why a module item is restricted.
The reviewer of the PR is freed from catching this subtle problematic code,
and can focus on reviewing other more important aspects of the code.
