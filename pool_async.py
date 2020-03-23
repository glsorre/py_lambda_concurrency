import logging
import asyncio

from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process
from threading import current_thread, Thread
from queue import Queue
from random import randint

logging.basicConfig(level=logging.INFO)

async def _run(p, counter):
    logging.info(f"{counter} {p.name}")
    await p.wait()
    logging.info(f"{counter} CLOSED")
    
async def _safe_run(p, counter, sem):
    async with sem:
        return await _run(p, counter)

async def _main_safe_run(q, sem):
    tasks = [
        asyncio.ensure_future(_safe_run(q[i], i, sem))
        for i
        in range(len(q))
    ]
    await asyncio.gather(*tasks)

class AsyncProcess(Process):
    def __init__(self, target, args):
        super().__init__(target=target, args=args)

    async def wait(self):
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        await loop.run_in_executor(None, self.start)
        await loop.run_in_executor(None, self.join)
        future.set_result(True)
        return future

class Pool:
    def __init__(self, max_workers):
        self.max_workers = max_workers
        self.threads = []
        self.queue = []
        self.sem = asyncio.Semaphore(max_workers)

    def map(self, func, args):
        for a in args:
            self.queue.append(AsyncProcess(target=func, args=(a, )))

        # for i in range(self.max_workers):
        #     t = Thread(target=_run, args=(self.queue, ))
        #     t.start()
        #     logging.info(f"{t.name} STARTED")
        #     self.threads.append(t)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_main_safe_run(self.queue, self.sem))
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

        # executor = ThreadPoolExecutor(self.max_workers)
        # prova = executor.map(_run, self.queue)

        #self.queue.join()

        # for i in range(self.max_workers):
        #     self.queue.put(None)

        # executor.shutdown()

        # for t in self.threads:
        #     logging.info(f"{t.name} JOINED")
        #     t.join()