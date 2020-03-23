import asyncio

from multiprocessing import Process, Manager

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
    def __init__(self, target, args, id):
        self.results = args[1]
        self.id = id
        super().__init__(target=target, args=args)

    def get_result(self, future):
        super(AsyncProcess, self).join()
        future.set_result(self.results[self.id])

    async def wait(self):
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        await loop.run_in_executor(None, self.start)
        await loop.run_in_executor(None, self.get_result, future)
        return future

class Pool:
    def __init__(self, max_workers):
        self.max_workers = max_workers
        self.threads = []
        self.queue = []
        self.sem = asyncio.Semaphore(max_workers)
        self.manager = Manager()
        self.results = self.manager.dict()

    def map(self, func, args):
        for i, a in enumerate(args):
            self.queue.append(AsyncProcess(target=func, args=(a, self.results, i), id=i))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(_main_safe_run(self.queue, self.sem))
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()