# Namer
An advanced remapper that also handles scope effectively within functions, classes, etc.

> Author: **Doremi109** - https://github.com/Doremii109 <br>
> Channel Link: https://t.me/doratools_channel

---

## What it does

- **Scope-aware renaming.** Tracks the module scope, functions (including nested ones), arguments, classes and their attributes separately. Correctly handles `global` / `nonlocal`, the walrus operator (`:=`), `except ... as`, and `match` patterns (`MatchAs`, `MatchStar`, `MatchMapping`).
- **Minified output.** Patches the stock `ast._Unparser` (on 3.14+ - `_ast_unparse.Unparser`) by rewriting the constants in its methods so that `ast.unparse` strips redundant spaces and indentation (`", "` → `","`, `" = "` → `"="`, a 4-space indent -> 1, and so on).
- **`__init__` hiding.** The `skipInit` pass renames `__init__` and hides the call either via `locals().update(...)` (if the class already has a metaclass) or via a generated metaclass whose `__call__` creates the object itself and invokes the renamed initializer.
- **kwargs remapping.** Keyword arguments at call sites are renamed consistently with the signatures of functions and constructors (`__init__`).
- **Optional builtins remapping.** With the `built` flag, references to built-in names are replaced and a header like `_0xN,... = len,range,...` is prepended.

## What it leaves alone

- Magic names (`__like_this__`) and `visit_*` methods (so as not to break ast-based code).
- `super`.
- External attributes and kwargs: attribute access on non-`self`/non-`cls` objects and keyword arguments of non-local function calls - they are collected into `pr_attr` automatically during `PreScan`.
- Any names in the `pr_var` / `pr_attr` whitelists.

## Requirements

- Python >= 3.10


## Usage

```python
from namer import rename

src = open("tester.py", encoding="utf8").read()
out = rename(src, track_instances=True)
open("tester_obf.py", "w", encoding="utf8").write(out)
```

Running the module directly reads `DVM.py` and writes the result to `OBFBBFFBFB.py` (see the `__main__` block).

### API

```python
rename(code, built=False, track_instances=False)
```

| Parameter         | Type                         | Purpose                                                                                                      |
|-------------------|------------------------------|--------------------------------------------------------------------------------------------------------------|
| `code`            | `str \| ast.Module`          | Source or AST. A string returns a string; an `ast.Module` returns an AST.                                    |
| `built`           | `bool \| dict`               | `False` - leave builtins untouched; `__builtins__` - remap them and prepend a header with the reassignments. |
| `track_instances` | `bool`                       | Remaps attributes reached via `var = SomeClass(...)`. Caution: can sometimes break obfuscated code.          |

### Whitelists

Two module-level sets control what to leave untouched (populated by the caller before `rename`):

- `pr_var` - names of variables/functions/classes that must not be renamed;
- `pr_attr` - attribute names that must not be renamed (`PreScan` extends it with the external attributes it finds).

## How it works
Everything happens inside the `rename` function:
1. **`PreScan`** - classifies names: class attributes (`cl_attr`), external attributes/kwargs (`pr_attr`), `self`/`cls` parameters per class (`slf_n`), and, with `track_instances`, local instance variables (`inst_vars`).
2. **`CollectNames`** - walks the tree with a scope stack and assigns new names, recording argument maps (`args_mp`) and obfuscated class names (`cls_obf`).
3. **`ReplNames`** - substitutes the new names at use sites (Load), resolving them through the scope stack, and consistently fixes up keyword arguments.
4. **`BuiltR`** (if `built` is set) - replaces references to builtins and builds the header.

`skipInit` is applied to the tree after `ReplNames`. Otherwise it would break `track_instances` when that is enabled.

## Limitations

- **`track_instances`** - a heuristic based on local-class constructors; it can get things wrong on non-trivial code.
