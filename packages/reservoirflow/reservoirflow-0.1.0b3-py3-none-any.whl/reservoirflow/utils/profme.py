"""
profme
======

This module is used to provide profiling functions.
"""

__all__ = [
    "cProfiler",
    "lProfiler",
    "profile",
    "timeit",
]

import os
import sys
import cProfile
import io
import pstats
import re
import time
from functools import wraps

import pandas as pd
from line_profiler import LineProfiler


def get_path():
    try:
        eval('__IPYTHON__')
        return os.getcwd()
    except NameError:
        return sys.path[0]

def cProfiler(sort_stats="tottime", print_output=True, save_output=False):
    """cProfile decorator.

    Parameters
    ----------
    sort_stats : str, optional
        sort table values by ['tottime', 'cumtime', 'ncalls', 'percall']
    print_output : bool, optional
        print output as a dataframe.
    save_output : bool, optional
        save output as csv file in the current working dir. The file
        name will be 'cProfiler_{function_name}.csv'.
    """
    # Backup:
    # - Other ways to store csv:
    #     1. using csv module: result must be a list
    #             with open(
    #                 f"profile_{func.__qualname__}.csv", mode="w", newline=""
    #             ) as f:
    #                 writer = csv.writer(f, delimiter=",")
    #                 writer.writerows([r.split(",") for r in result])
    #     2. using pandas:
    #             data = io.StringIO("\n".join(result))
    #             df = pd.read_csv(data, sep=",")
    #             df.to_csv(f"profile_{func.__qualname__}.csv", index=False)

    def decorator(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            pr = cProfile.Profile()
            s = io.StringIO()
            pr.enable()
            _func = func(*args, **kwargs)
            pr.disable()
            stats = pstats.Stats(pr, stream=s).sort_stats(sort_stats)
            stats.print_stats()
            result = s.getvalue()
            result = [l.strip() for l in re.split("\n+", result)][2:-1]
            result = [re.sub(r"\s+", ",", r, count=5) for r in result]
            if print_output:
                data = io.StringIO("\n".join(result))
                df = pd.read_csv(data, sep=",")
                print("\n\n", df)
            if save_output:
                file_name = f"cProfiler_{func.__qualname__}.csv"
                path = os.path.join(get_path(), file_name)
                with open(path, mode="w") as f:
                    f.write("\n".join(result))
            return _func

        return wrapped_func

    return decorator


def lProfiler(print_output=True, save_output=False):
    """lProfiler (line profiler) decorator.

    Parameters
    ----------
    print_output : bool, optional
        print output as a dataframe.
    save_output : bool, optional
        save output as csv file in the current working dir. The file
        name will be 'lProfiler_{function_name}.csv'.
    """
    # Backup
    # ------
    # - info can also be accessed in indices range(0:4):
    #     info = "\n ".join(result[:4])
    #     print("[info]:\n", info)

    def decorator(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            pr = LineProfiler()
            _func = pr(func)(*args, **kwargs)
            s = io.StringIO()
            pr.print_stats(stream=s)
            result = s.getvalue()
            if print_output:
                print(result)
            if save_output:
                result = [l.strip() for l in re.split("\n+", result)]
                head = re.findall(r"\S+ ?\S+", result[4])
                iter = [
                    [m.start(), m.end()] for m in re.finditer(r"\S+ ?\S+", result[4])
                ]
                iter[-1][1] = None
                lines = [
                    ",".join([l[h[0] : h[1]].strip() for h in iter]) for l in result[6:]
                ]
                lines[0] = re.sub(", ", "; ", lines[0])
                file_name = f"lProfiler_{func.__qualname__}.csv"
                path = os.path.join(get_path(), file_name)
                with open(path, mode="w") as f:
                    f.write(",".join(head) + "\n")
                    f.write("\n".join(lines))

            return _func

        return wrapped_func

    return decorator


def profile(func):
    """line profiler decorator.

    Notes
    -----
    https://gist.github.com/pavelpatrin/5a28311061bf7ac55cdd
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        prof = LineProfiler()
        try:
            return prof(func)(*args, **kwargs)
        finally:
            prof.print_stats()

    return wrapper


def timeit(func):
    # reference: https://stackoverflow.com/a/27737385/11549398
    @wraps(func)
    def wrap(*args, **kw):
        ts = time.time()
        result = func(*args, **kw)
        te = time.time()
        # print("func:%r args:[%r, %r] took: %2.4f sec" % (func.__name__, args, kw, te - ts))
        print("\n\nfunc:%r took: %2.4f sec" % (func.__name__, te - ts))
        return result

    return wrap


if __name__ == "__main__":
    # @timeit
    # @cProfiler(print_output=True)
    # @profile
    @lProfiler(print_output=False, save_output=True)
    def sum_numbers(n):
        sum = 0
        for a in range(n):
            sum += a
        return sum

    a = sum_numbers(100000)
    print(a)
