import logging
import asyncio

from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process
from threading import current_thread, Thread
from queue import Queue

logging.basicConfig(level=logging.INFO)

async def _run(p, counter):
    # while True:
    logging.info(f"{counter} {p.name}")
    #     # logging.info(f"{current_thread().name}")
    #     p = q.get()
    #     if p is None:
    #         break
    p.start()
    p.join()
    p.close()
    while p.is_alive():
        await asyncio.sleep(0.01)
    logging.info(f"CLOSED")
    
    #q.task_done()
    
async def _safe_run(p, counter, sem):
    logging.info(sem)
    async with sem:
        logging.info("INNNNNNNNNNNNNNNNNNNNNNNNNN")
        return await _run(p, counter)

async def _main_safe_run(q, sem):
    logging.info(sem)
    tasks = [
        asyncio.ensure_future(_safe_run(q[i], i, sem))
        for i
        in range(len(q))
    ]
    await asyncio.gather(*tasks)      

class Pool:
    def __init__(self, max_workers):
        self.max_workers = max_workers
        self.threads = []
        self.queue = []
        self.sem = asyncio.Semaphore(max_workers)

    def map(self, func, args):
        counter = len(args)

        for a in args:
            self.queue.append(Process(target=func, args=(a, )))

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