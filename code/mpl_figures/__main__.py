#!/usr/bin/env python2
# encoding: utf-8

import glob
import os
import os.path as osp
import sys

sys.path.insert(0, osp.dirname(osp.abspath(__file__)))

from . import core
from .core import log


def plot_all():
    plotscripts = glob.glob(osp.join(osp.dirname(osp.abspath(__file__)),
        "fig*.py"))

    plotscripts = map(lambda x: osp.splitext(osp.basename(x))[0], plotscripts)

    for name in plotscripts:
        core.make_figure(name)


if __name__ == "__main__":
    import sys
    from inspect import isfunction, getargspec
    local_globals = globals().keys()

    def is_noarg_function(f):
        "Test if f is valid function and has no arguments"
        func = globals()[f]
        if isfunction(func):
            argspec = getargspec(func)
            if len(argspec.args) == 0\
                        and argspec.varargs is None\
                        and argspec.keywords is None:
                return True
        return False

    def show_functions():
        functions.sort()
        for f in functions:
            print f
    functions = [f for f in local_globals if is_noarg_function(f)]
    if len(sys.argv) <= 1 or sys.argv[1] == "-h":
        show_functions()
    else:
        for launch in sys.argv[1:]:
            if launch in functions:
                run = globals()[launch]
                run()
            else:
                print launch, "not part of functions:"
                show_functions()
