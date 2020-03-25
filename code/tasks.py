from urllib import request

from constants import *
from sort import quick_sort, selection_sort

def counted(f):
    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        return f(*args, **kwargs)
    wrapped.calls = 0
    return wrapped

@counted
def io_bounded_func(url=IO_TASK_URL):
    return request.urlopen(url)

@counted
def cpu_bounded_func(n=CPU_FUNC_NUMBER):
    return selection_sort(n)

@counted
def cpu_bounded_func_quick(n=CPU_FUNC_NUMBER):
    return quick_sort(n)