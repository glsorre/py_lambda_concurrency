import logging
import asyncio

from multiprocessing import Process, Queue

logging.basicConfig(level=logging.INFO)

async def _run(p, counter):
    return await p.wait()

async def _safe_run(p, counter, sem):
    async with sem:
        return await _run(p, counter)

async def _main_safe_run(q, sem):
    tasks = [
        asyncio.ensure_future(_safe_run(q[i], i, sem))
        for i
        in range(len(q))
    ]
    return await asyncio.gather(*tasks)

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

        loop = asyncio.get_event_loop()
        prova = loop.run_until_complete(_main_safe_run(self.queue, self.sem))
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

        for test in prova:
            print(test)