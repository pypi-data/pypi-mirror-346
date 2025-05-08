import sys
import runpy

runpy.run_module(
    "fixthis_internal.interpreter",
    run_name="__main__",
    alter_sys=False,
)
sys.exit()
