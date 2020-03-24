from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from math import factorial
from timeit import timeit
from urllib import request

from pool_thread import Pool

CPU_TOT_NUMBER = 20000
CPU_FUNC_NUMBER = 5000
CPU_POOL_SIZE = 24
IO_TOT_NUMBER = 10
IO_POOL_SIZE = 12

def cpu_bounded_func(n):
    return factorial(n)

def cpu_bounded_func_result(n, results, index):
    result = factorial(n)
    results[index] = result
    return result

def io_bounded_func(url):
    return request.urlopen(url)

def sequential_io_handler(event={}, lambda_context={}):
    for url in range(IO_TOT_NUMBER):
        io_bounded_func('https://docs.python.org/3/')

def sequential_cpu_handler(event={}, lambda_context={}):
    for i in range(CPU_TOT_NUMBER):
        cpu_bounded_func(CPU_FUNC_NUMBER)

def thread_io_handler(event={}, lambda_context={}):
    executor = ThreadPoolExecutor(max_workers=IO_POOL_SIZE)
    executor.map(io_bounded_func, ['https://docs.python.org/3/' for x in range(IO_TOT_NUMBER)])
    executor.shutdown()

def thread_cpu_handler(event={}, lambda_context={}):
    executor = ThreadPoolExecutor(max_workers=5)
    executor.map(cpu_bounded_func, [CPU_TOT_NUMBER for x in range(CPU_FUNC_NUMBER)])
    executor.shutdown()

def process_io_handler(event={}, lambda_context={}):
    executor = ProcessPoolExecutor(max_workers=IO_POOL_SIZE)
    executor.map(io_bounded_func, ['https://docs.python.org/3/' for x in range(IO_TOT_NUMBER)])
    executor.shutdown()

def process_cpu_handler(event={}, lambda_context={}):
    executor = ProcessPoolExecutor(max_workers=CPU_POOL_SIZE)
    executor.map(cpu_bounded_func, [CPU_FUNC_NUMBER for x in range(CPU_TOT_NUMBER)])
    executor.shutdown()

def process_cpu_handler_no_executor(event={}, lambda_context={}):
    data = [CPU_FUNC_NUMBER for x in range(CPU_TOT_NUMBER)]
    pool = Pool(CPU_POOL_SIZE)
    pool.map(cpu_bounded_func, data)

def lambda_handler(event, lambda_context):
    if event.get("io_sequential", "False") == "True":
        sequential_io_handler()
    elif event.get("io_threaded", "False") == "True":
        thread_io_handler()
    elif event.get("io_process", "False") == "True":
        process_io_handler()
    elif event.get("cpu_sequential", "False") == "True":
        sequential_cpu_handler()
    elif event.get("cpu_threaded", "False") == "True":
        thread_cpu_handler()
    elif event.get("cpu_process", "False") == "True":
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
