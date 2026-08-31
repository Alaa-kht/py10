*This project has been created as part of the 42 curriculum by aalkhati.*

# Python Module 10 — FuncMage (Functional Programming)

Five realms of functional Python: anonymous functions, higher-order
functions, closures and lexical scoping, the functools module, and
decorators with @staticmethod. No external libraries, no globals,
no file I/O — pure functional patterns.

## Project structure

```
py10/
├── README.md
├── ex0/
│   └── lambda_spells.py         # Lambda expressions for data transformation
├── ex1/
│   └── higher_magic.py          # Functions taking and returning functions
├── ex2/
│   └── scope_mysteries.py       # Closures, lexical scoping, nonlocal
├── ex3/
│   └── functools_artifacts.py   # reduce, partial, lru_cache, singledispatch
└── ex4/
    └── decorator_mastery.py     # Custom decorators + @staticmethod
```

## How to run

Each exercise is a standalone script, no installation required:

```bash
python3 ex0/lambda_spells.py
python3 ex1/higher_magic.py
python3 ex2/scope_mysteries.py
python3 ex3/functools_artifacts.py
python3 ex4/decorator_mastery.py
```

Requirements: Python 3.10+. Only standard library and built-ins are
used — `functools`, `operator`, `typing`, `collections.abc` where
specified per exercise.

## The exercises

### ex0 — Lambda Sanctum (anonymous functions)

Four functions demonstrating lambda expressions for one-time data
transformations, never assigned to a name (which both defeats the
purpose and trips flake8 E731): `artifact_sorter` uses `sorted()`
with a lambda key to rank artifacts by power, descending;
`power_filter` uses `filter()` with a lambda test to keep mages at or
above a power threshold; `spell_transformer` uses `map()` with a
lambda to wrap each spell name in `"* "` / `" *"`; `mage_stats` uses
lambdas with `max()`/`min()` (which return the whole matching dict,
indexed into for just the value) plus `sum()`/`len()`/`round()` for
the average. `filter()` and `map()` return lazy iterators, wrapped in
`list()` to match the required return types.

### ex1 — Higher Realm (higher-order functions)

Demonstrates that functions are first-class citizens: passed as
arguments, returned from other functions, stored in variables. Every
function follows the pattern *outer takes function(s) → defines an
inner function → returns the inner function itself, never called*.
`spell_combiner` calls two spells with the same arguments and returns
a tuple of both results. `power_amplifier` multiplies the power
argument before delegating to the original spell. `conditional_caster`
only casts if a condition function (called with the same arguments)
returns True, else returns `"Spell fizzled"`. `spell_sequence` casts
every spell in a list and collects the results. `Callable` is
imported from `collections.abc` (the current, non-deprecated source,
as opposed to `typing.Callable`).

### ex2 — Memory Depths (closures and lexical scoping)

A closure is a function that remembers variables from the scope it
was created in, even after that scope has finished executing.
`mage_counter` keeps a private `count` that persists between calls via
`nonlocal` — each call to `mage_counter()` creates an independent
counter with its own state, proven by `counter_a` and `counter_b`
counting separately. `spell_accumulator` closes over a running total,
adding to it on each call. `enchantment_factory` closes over the
enchantment type string, producing differently-flavored functions
from the same code. `memory_vault` closes over a private dict,
exposing only `store`/`recall` functions — the dict itself is never
directly accessible from outside, an encapsulation pattern achieved
without a class. `nonlocal` is required wherever an enclosing
variable is reassigned (not just read); `global` remains forbidden,
since closures are exactly the tool that avoids needing module-level
mutable state.

### ex3 — Ancient Library (functools treasures)

`spell_reducer` uses `functools.reduce` with `operator` functions
(`add`, `mul`) and the builtins `max`/`min`, selected from a dict by
operation name; empty input returns 0, an unknown operation raises
`ValueError`. `partial_enchanter` uses `functools.partial` to
pre-fill `power=50` and an element name on a base three-argument
function, producing three specialized single-argument versions.
`memoized_fibonacci` uses `@functools.lru_cache` so repeated calls
with the same `n` are served from cache instead of recomputing —
essential for recursive Fibonacci, which otherwise recalculates the
same values exponentially many times. `spell_dispatcher` uses
`@functools.singledispatch` to route to different implementations
based on the runtime type of the argument (int/str/list, plus an
`Any`-typed fallback for unregistered types), returning the
dispatcher function itself rather than calling it.

### ex4 — Master's Tower (decorators and @staticmethod)

Every decorator follows the same three-part shape as ex1's
higher-order functions, plus `@functools.wraps(func)` on the inner
wrapper to preserve the original function's `__name__` and docstring
(without it, introspection would report `"wrapper"` instead of the
real name). `spell_timer` times execution with `time.time()`,
printing before/after messages with the elapsed time to 3 decimals.
`power_validator(min_power)` is a decorator *factory* — three levels
of nesting instead of two, because `@power_validator(10)` first calls
`power_validator(10)`, which must return an actual decorator — that
checks a power value found positionally or by keyword and blocks the
call with `"Insufficient power for this spell"` if it is too low.
Reading power as `kwargs.get("power", args[-1])` rather than a fixed
index makes the same decorator work on both a plain function and an
instance method, where `self` shifts every positional index by one.
`retry_spell(max_attempts)` retries a failing function up to a limit,
printing a retry message between attempts (but not after the final
one) and returning a failure message if every attempt raises.
`MageGuild.validate_mage_name` is a `@staticmethod` — no `self`, pure
utility, callable directly on the class — while `cast_spell` is a
normal instance method decorated with `@power_validator(10)`.

## Code quality

```bash
flake8 .    # passes clean
mypy .      # passes clean on every exercise, including inner/nested
            # function signatures (not just the outer functions)
```

All five programs reproduce the subject's example outputs, including
the retry failure sequence and the power-validator rejection message.

## Concepts covered

- **Lambda expressions**: anonymous, single-expression functions used
  inline as arguments — never named, never containing statements.
- **Higher-order functions**: functions that accept and/or return
  other functions; the mechanism behind `sorted`/`filter`/`map` and
  every decorator.
- **Closures**: an inner function retains access to its enclosing
  scope's variables after that scope returns; `nonlocal` is required
  to reassign (not just read) an enclosing variable.
- **functools.reduce / partial / lru_cache / singledispatch**: four
  distinct patterns — aggregate a sequence, pre-fill arguments,
  memoize by argument, and dispatch by runtime type.
- **Decorators**: wrap a function to add behavior around it without
  modifying its source; `*args, **kwargs` let a wrapper forward any
  signature; `functools.wraps` preserves the wrapped function's
  identity.
- **@staticmethod**: a method that needs no `self` and no instance
  data, organized inside a class purely for namespacing.

## Design choices worth noting

- Every lambda is passed inline as an argument rather than assigned
  to a name, per the subject's explicit requirement and to avoid
  flake8 E731.
- `power_validator` reads the power argument by keyword-first,
  positional-last (`kwargs.get("power", args[-1])`) rather than a
  fixed index, so the identical decorator works correctly on a
  standalone function and on an instance method with `self` shifting
  the argument positions.
- `memory_vault`'s dict is never exposed directly — only the
  `store`/`recall` closures are returned — demonstrating
  encapsulation achieved through closures rather than a class.
- `retry_spell` only prints the retry message when attempts remain,
  so the final failed attempt goes straight to the failure message
  without an extra, misleading "retrying" line.
