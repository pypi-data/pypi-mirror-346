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
```

## Testing

To run the test:

    make test

The Makefile's `test` target prepends `venv/bin` to your PATH so it will use the Python in `venv/bin/python` if you have a local virtualenv named `venv`.

Or directly:

    PYTHONPATH=src python tests/basic_test.py

If it exits with a non-zero exit code, and no exception is printed, the Tests should have passed. If not, good luck!
