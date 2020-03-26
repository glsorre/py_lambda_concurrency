import logging
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count as thread_count
from os import cpu_count
from threading import Thread, Timer
from time import time
from random import randint
from urllib import request

import tasks
from pool_thread import Pool

logging.basicConfig(level=logging.INFO)

INTERVAL = 20

def ops_logger(f, c, results):
    results['ops'][INTERVAL * c] = f.calls.value
    logging.info(f"At {INTERVAL * c} seconds: {f.calls.value} operations done")
    c += 1
    t = Timer(INTERVAL, ops_logger, (f, c, results))
    t.daemon = True
    t.start()
    return t

def lambda_handler(event, lambda_context):
    results = {}
    start_time = time()

    executor = event['executor']
    pool_size = thread_count() + 2 if event['pool_size'] == 'cpu_count' else event['pool_size']
    tot_number = event['tot_number']
    function_name = event['function_name']
    function_arg = eval(event['function_arg'])

    logging.info(f"CPUs available: {cpu_count()}, Logical cores: {thread_count()}")
    logging.info(f"Running executor: {executor} for a total of {tot_number} operations")
    logging.info(f"Function name: {function_name}")
    logging.info(f"Pool max_workers: {pool_size} if applicable")

    results['cpu_count'] = cpu_count()
    results['logical_cpu_count'] = thread_count()
    results['executor'] = executor
    results['tot_number'] = tot_number
    results['function_name'] = function_name
    results['function_arg'] = function_arg
    results['pool_size'] = pool_size
    results['ops'] = {}

    t = ops_logger(getattr(tasks, function_name), 0, results)

    if executor == 'sequential':
        for i in range(tot_number):
            getattr(tasks, function_name)(function_arg)
    elif executor == 'threadpool':
        executor = ThreadPoolExecutor(max_workers=pool_size)
        executor.map(getattr(tasks, function_name), [function_arg for x in range(tot_number)])
        executor.shutdown()
    else:
        pool = Pool(pool_size)
        data = [function_arg for x in range(tot_number)]
        pool.map(getattr(tasks, function_name), data)
        pool.close()

    t.join()
    results['final_time'] = time() - start_time
    logging.info(f"Total number of calls to function: {getattr(tasks, function_name).calls.value}")
    return results

if __name__ == "__main__":
    event = {
        'executor': 'sequential',
        'pool_size': 'cpu_count',
        'tot_number': 100,
        'function_name': 'cpu_bounded_func',
        'function_arg': "[randint(10, 10000) for x in range(10000)]"
    }
    start = time()
    results = lambda_handler(event, {})
    logging.info(time() - start)
    logging.info(results)
