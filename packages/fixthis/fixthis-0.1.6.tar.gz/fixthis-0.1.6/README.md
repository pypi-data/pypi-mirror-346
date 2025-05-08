# PYTHON-FIXTHIS

This is a small Python library that adds a simple AST-based name fixer/interpreter for Python scripts.

## Implemented Features

Currently, only english numbers(use a variable name like `five_hundred_eight`
and have it contain the value 508), and a fallback where undefined variables just
have their own name as a string value

```python
import fixthis
print(Hello == 'Hello') # True
print(forty_seven_million) # 47000000
print(LATIN_SMALL_LETTER_E_WITH_ACUTE) # é Named unicode, all caps
# Or compounds, separated by __
print(The_equation__COLON__SPACE__four__PLUS__seven__IS__nineteen___IS_INCORRECT)
# The equation: 4+7=11 IS INCORRECT
```

## Testing

To run the test:

    make test

The Makefile's `test` target prepends `venv/bin` to your PATH so it will use the Python in `venv/bin/python` if you have a local virtualenv named `venv`.

Or directly:

    PYTHONPATH=src python tests/basic_test.py

If it exits with a non-zero exit code, and no exception is printed, the Tests should have passed. If not, good luck!
