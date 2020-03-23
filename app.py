from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from math import factorial
from timeit import timeit
from urllib import request

from pool_thread import Pool

def cpu_bounded_func(n):
    return factorial(n)

def cpu_bounded_func_result(n, results, index):
    result = factorial(n)
    results[index] = result
    return result

def io_bounded_func(url):
    return request.urlopen(url)

def sequential_io_handler(event={}, lambda_context={}):
    for url in range(10):
        io_bounded_func('https://docs.python.org/3/')

def sequential_cpu_handler(event={}, lambda_context={}):
    for i in range(5000):
        cpu_bounded_func(5000)

def thread_io_handler(event={}, lambda_context={}):
    executor = ThreadPoolExecutor(max_workers=5)
    executor.map(io_bounded_func, ['https://docs.python.org/3/' for x in range(10)])
    executor.shutdown()

def thread_cpu_handler(event={}, lambda_context={}):
    executor = ThreadPoolExecutor(max_workers=5)
    executor.map(cpu_bounded_func, [5000 for x in range(5000)])
    executor.shutdown()

def process_io_handler(event={}, lambda_context={}):
    executor = ProcessPoolExecutor(max_workers=5)
    executor.map(io_bounded_func, ['https://docs.python.org/3/' for x in range(10)])
    executor.shutdown()

def process_cpu_handler(event={}, lambda_context={}):
    executor = ProcessPoolExecutor(max_workers=5)
    executor.map(cpu_bounded_func, [5000 for x in range(5000)])
    executor.shutdown()

def process_cpu_handler_no_executor(event={}, lambda_context={}):
    data = [5000 for x in range(5000)]
    pool = Pool(5)
    pool.map(cpu_bounded_func, data)

def lambda_handler(event, lambda_context):
    if event["io_sequential"] == True:
        sequential_io_handler()
    elif event["io_threaded"] == True:
        thread_io_handler()
    elif event["io_process"] == True:
        process_io_handler()
    if event["cpu_sequential"] == True:
        sequential_cpu_handler()
    elif event["cpu_threaded"] == True:
        thread_cpu_handler()
    elif event["cpu_process"] == True:
        process_cpu_handler()
    else:
        process_cpu_handler_no_executor()
    
if __name__ == "__main__":
    count = 1
    print("*** IO Task ***")
    print("Sequential", timeit(sequential_io_handler, number=count))
    print("Threaded", timeit(thread_io_handler, number=count))
    print("Multiprocess", timeit(process_io_handler, number=count))
    print("*** CPU Task ***")
    print("Sequential", timeit(sequential_cpu_handler, number=count))
    print("Threaded", timeit(thread_cpu_handler, number=count))
    print("Multiprocess", timeit(process_cpu_handler, number=count))
    print("Multiprocess no executor", timeit(process_cpu_handler_no_executor, number=count))
