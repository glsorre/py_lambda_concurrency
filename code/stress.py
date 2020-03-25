import logging
from concurrent.futures import ThreadPoolExecutor
from os import cpu_count
from threading import Thread, Timer
from time import time
from random import randint
from urllib import request

import tasks
from pool_thread import Pool

logging.basicConfig(level=logging.INFO)

def ops_logger(f, c):
    c += 1
    logging.info(f"At {20 * c} seconds: {f.calls} operations done")
    t = Timer(20, ops_logger, (f, c, ))
    t.daemon = True
    t.start()

def lambda_handler(event, lambda_context):
    executor = event['executor']
    pool_size = cpu_count() if event['pool_size'] == 'cpu_count' else event['pool_size']
    tot_number = event['tot_number']
    function_name = event['function_name']
    function_arg = eval(event['function_arg'])

    logging.info(f"CPUs available: {cpu_count()}")
    logging.info(f"Running executor: {executor} for a total of {tot_number} operations")
    logging.info(f"Function name: {function_name} with the following {function_arg} argument")
    logging.info(f"Pool max_workers: {pool_size} if applicable")

    ops_logger(getattr(tasks, function_name), 0)

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

    logging.info(f"Total number of calls to function: {getattr(tasks, function_name).calls}")

if __name__ == "__main__":
    event = {
        'executor': 'threadpool',
        'pool_size': 'cpu_count',
        'tot_number': 20,
        'function_name': 'io_bounded_func',
        'function_arg': "'https://docs.python.org/3/'"
    }
    start = time()
    lambda_handler(event, {})
    logging.info(time() - start)
