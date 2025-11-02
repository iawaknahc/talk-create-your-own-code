## Create your own code

Code means **rules** here

---

###### What is it?

Create your own rules with **linter**

To forbid **problematic** pattern in codebase

---

###### What are the alternatives?

- Clever use of the type system
- Exhaustive tests

---

###### Clever use of the type system

- Make illegal states unrepresentable.

_But this technique only applies to the code you write._

---

###### Exhaustive tests

- AI helps us write many **example-based** tests

_But these tests are not exhaustive._

---

###### Case study: URL parsing in Python

Live code demo

---

###### The root problem

- Cannot be guarded by type checking.
- We rarely test the behavior of stdlib functions.

---

###### The solution

- Forbid the use of `urlparse` and `urlunparse`

---

###### Case study: Celery

Live code demo

---

###### The problem

- Incorrect use of `celery.group`

---

###### The solution

- Forbid the use of `celery.group`

---

###### How?

Write our own Pylint custom checker

---

###### Case study: Default timezone in Go

Live code demo

---

###### The problem

- The default timezone in Go is `Local` while our project wants `UTC`.

---

###### The solution

- Forbid time construction without `.UTC()`

---

###### How?

Write our own Go analyzer

---

# Q & A

---

# Thank you
