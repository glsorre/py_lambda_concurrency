from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from random import randint
from sort import selection_sort as sort
from timeit import timeit
from urllib import request

from pool_thread import Pool

CPU_TOT_NUMBER = 10
CPU_FUNC_NUMBER = [randint(1, 10000) for x in range(10000)]
CPU_POOL_SIZE = 4
IO_TOT_NUMBER = 12
IO_POOL_SIZE = 4
IO_TASK_URL = 'https://docs.python.org/3/'

def io_bounded_func(url=IO_TASK_URL):
    return request.urlopen(url)

def cpu_bounded_func(n=CPU_FUNC_NUMBER):
    return sort(n)

def sequential_io_handler(event={}, lambda_context={}):
    for url in range(IO_TOT_NUMBER):
        io_bounded_func(IO_TASK_URL)

def sequential_cpu_handler(event={}, lambda_context={}):
    for i in range(CPU_TOT_NUMBER):
        cpu_bounded_func(CPU_FUNC_NUMBER)

def thread_io_handler(event={}, lambda_context={}):
    executor = ThreadPoolExecutor(max_workers=IO_POOL_SIZE)
    executor.map(io_bounded_func, [IO_TASK_URL for x in range(IO_TOT_NUMBER)])
    executor.shutdown()

def thread_cpu_handler(event={}, lambda_context={}):
    executor = ThreadPoolExecutor(max_workers=CPU_POOL_SIZE)
    executor.map(cpu_bounded_func, [CPU_FUNC_NUMBER for x in range(CPU_TOT_NUMBER)])
    executor.shutdown()

def process_io_handler(event={}, lambda_context={}):
    executor = ProcessPoolExecutor(max_workers=IO_POOL_SIZE)
    executor.map(io_bounded_func, [IO_TASK_URL for x in range(IO_TOT_NUMBER)])
    executor.shutdown()

def process_cpu_handler(event={}, lambda_context={}):
    executor = ProcessPoolExecutor(max_workers=CPU_POOL_SIZE)
    executor.map(cpu_bounded_func, [CPU_FUNC_NUMBER for x in range(CPU_TOT_NUMBER)])
    executor.shutdown()

def process_io_handler_no_executor(event={}, lambda_context={}):
    data = [IO_TASK_URL for x in range(IO_TOT_NUMBER)]
    pool = Pool(IO_POOL_SIZE)
    pool.map(io_bounded_func, data)
    pool.close()

def process_cpu_handler_no_executor(event={}, lambda_context={}):
    pool = Pool(CPU_POOL_SIZE)
    data = [CPU_FUNC_NUMBER for x in range(CPU_TOT_NUMBER)]
    pool.map(cpu_bounded_func, data)
    pool.close()

def lambda_handler(event, lambda_context):
    if event.get("io_sequential", "False") == "True":
        print("*** io_sequential")
        sequential_io_handler()
    elif event.get("io_threaded", "False") == "True":
        print("*** io_threaded")
        thread_io_handler()
    elif event.get("io_process", "False") == "True":
        print("*** io_process")
        process_io_handler()
    elif event.get("io_process_no_executor", "False") == "True":
        print("*** io_process_no_executor")
        process_io_handler_no_executor()
    elif event.get("cpu_sequential", "False") == "True":
        print("*** cpu_sequential")
        sequential_cpu_handler()
    elif event.get("cpu_threaded", "False") == "True":
        print("*** cpu_threaded")
        thread_cpu_handler()
    elif event.get("cpu_process", "False") == "True":
        print("*** cpu_process")
        process_cpu_handler()
    else:
        print("*** cpu_process_no_executor")
        process_cpu_handler_no_executor()
    
if __name__ == "__main__":
    count = 1
    print("*** IO Task Duration", timeit(io_bounded_func, number=count))
    print("*** CPU Task Duration", timeit(cpu_bounded_func, number=count))
    print("*** IO Task ***")
    print("Sequential", timeit(sequential_io_handler, number=count))
    print("Threaded", timeit(thread_io_handler, number=count))
    print("Multiprocess", timeit(process_io_handler, number=count))
    print("Multiprocess no executor", timeit(process_io_handler_no_executor, number=count))
    print("*** CPU Task ***")
    print("Sequential", timeit(sequential_cpu_handler, number=count))
    print("Threaded", timeit(thread_cpu_handler, number=count))
    print("Multiprocess", timeit(process_cpu_handler, number=count))
    print("Multiprocess no executor", timeit(process_cpu_handler_no_executor, number=count))
