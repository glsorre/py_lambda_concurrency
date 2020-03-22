from multiprocessing import Process
from threading import Thread
from queue import Queue

class Pool:
    def __init__(self, max_workers):
        self.max_workers = max_workers
        self.processes = []
        self.queue = Queue()

    def map(self, func, args):
        for arg in args:
            p = Process(target=func, args=(arg, ))
            self.queue.put(p)

        for i in range(self.max_workers):
            p = self.queue.get()
            p.start()                  
            self.processes.append(p)

        def create(processes, queue):
            
            while queue.qsize() > 0 and processes:
                alive_processes = [p for p in self.processes if p.is_alive()]
                for p in range(0, self.max_workers - len(alive_processes)):
                    p = queue.get()
                    p.start()                  
                    self.processes.append(p)

        create_thread = Thread(target=create, args=(self.processes, self.queue))

        def delete(processes, queue):
            
            while queue.qsize() > 0:
                dead_processes = [p for p in self.processes if not p.is_alive()]
                for p in dead_processes:
                    self.processes.remove(p)
                    p.join()
                    p.close()
            
        delete_thread = Thread(target=create, args=(self.processes, self.queue))

        create_thread.start()
        delete_thread.start()
        create_thread.join()
        delete_thread.join()

    def close(self):
        for p in self.processes:
            p.join()
            p.close()
