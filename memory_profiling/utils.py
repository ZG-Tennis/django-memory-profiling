# -*- coding: utf-8 -*-
""" memory_profiling's utils """

from __future__ import print_function
import sys


def output_function(o):
    """ returns a string representation of the object type """
    return str(type(o))


def memory_info(process):
    """
    psutil < 2.0 does not have memory_info, >= 3.0 does not have
    get_memory_info
    """
    return (getattr(process, 'memory_info', None) or process.get_memory_info)()


def warning(*objs):
    print("WARNING: ", *objs, file=sys.stderr)


def info(*objs):
    print("INFO: ", *objs, file=sys.stdout)
