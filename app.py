from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from math import factorial
from multiprocessing import Process
from queue import Queue
from random import randint
from timeit import timeit
from urllib import request

from pool_async import Pool

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
    for i in range(10000):
        cpu_bounded_func(5000)

def thread_io_handler(event={}, lambda_context={}):
    executor = ThreadPoolExecutor(max_workers=5)
    executor.map(io_bounded_func, ['https://docs.python.org/3/' for x in range(10)])
    executor.shutdown()

def thread_cpu_handler(event={}, lambda_context={}):
    executor = ThreadPoolExecutor(max_workers=5)
    executor.map(cpu_bounded_func, [5000 for x in range(10000)])
    executor.shutdown()

def process_io_handler(event={}, lambda_context={}):
    executor = ProcessPoolExecutor(max_workers=5)
    executor.map(io_bounded_func, ['https://docs.python.org/3/' for x in range(10)])
    executor.shutdown()

def process_cpu_handler(event={}, lambda_context={}):
    executor = ProcessPoolExecutor(max_workers=5)
    executor.map(cpu_bounded_func, [5000 for x in range(10000)])
    executor.shutdown()

def process_cpu_handler_no_executor(event={}, lambda_context={}):
    data = [5000 for x in range(500)]
    pool = Pool(5)
    pool.map(cpu_bounded_func_result, data)

if __name__ == "__main__":
    count = 1
    print("*** IO Task ***")
    # print("Sequential", timeit(sequential_io_handler, number=count))
    # print("Threaded", timeit(thread_io_handler, number=count))
    # print("Multiprocess", timeit(process_io_handler, number=count))
    # print("*** CPU Task ***")
    #print("Sequential", timeit(sequential_cpu_handler, number=count))
    #print("Threaded", timeit(thread_cpu_handler, number=count))
    #print("Multiprocess", timeit(process_cpu_handler, number=count))
    print("Multiprocess no executor", timeit(process_cpu_handler_no_executor, number=count))
