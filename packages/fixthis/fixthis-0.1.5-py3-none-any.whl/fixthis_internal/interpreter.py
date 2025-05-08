globals()["fixed"] = True
import sys
from ast import *
import inspect
import unicodedata as ucd
from fixthis_internal.name_utils import parse_english_number, parse_string

pypy = False  # No pypy support for now


class FixVisitor(NodeTransformer):
    def visit_Name(self, node):
        if not isinstance(node.ctx, Load):
            return node
        return Call(
            func=Name(id="___fixthis_internal_name___"),
            args=[
                Constant(value=node.id),
                Call(func=Name(id="locals", ctx=Load()), keywords=[], args=[]),
                Call(func=Name(id="globals", ctx=Load()), keywords=[], args=[]),
                (
                    Attribute(
                        value=Name(id="__builtins__", ctx=Load()),
                        attr="__dict__",
                        ctx=Load(),
                    )
                    if pypy
                    else (Name(id="__builtins__", ctx=Load()))
                ),
            ],
            keywords=[],
        )

    #    def visit_Raise(self, node): ...


_args = sys.argv
if len(_args) > 1:
    source_file = _args[1]
else:
    source_file = _args[0]

with open(source_file, "r", encoding="utf-8") as f:
    source = f.read()

source_tree = FixVisitor().visit(parse(source, filename=source_file))
source_tree = fix_missing_locations(source_tree)


# helper to resolve names at runtime
def ___fixthis_internal_name___(varname, *scopes):
    for scope in scopes:
        if varname in scope:
            return scope[varname]

    return parse_string(varname)


compiled = compile(source_tree, source_file, mode="exec")

# execution environment including helper function
env = {
    "__name__": "__main__",
    "__doc__": None,
    "__package__": None,
    "__loader__": None,
    "__spec__": ("python-fixthis", 0, 1, 5),
    "__annotations__": {},
    "__file__": source_file,
    "__cached__": None,
    "fixed": True,
    "___fixthis_internal_name___": ___fixthis_internal_name___,
}
exec(compiled, env)
