import threading
import queue
import time
import uuid
class DivineProcess:
    def __init__(self, name, target, args=(), priority=0):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.target = target
        self.args = args
        self.priority = priority
        self.state = "created"
        self.thread = None
        self.execution_count = 0
    def start(self):
        self.state = "running"
        self.thread = threading.Thread(target=self.target, args=self.args, daemon=True)
        self.thread.start()
    def is_alive(self):
        return self.thread is not None and self.thread.is_alive()
class DivineScheduler:
    def __init__(self):
        self.processes = {}
        self.ready_queue = queue.PriorityQueue()
        self.lock = threading.Lock()
        self.running = False
    def create_process(self, name, target, args=(), priority=0):
        process = DivineProcess(name, target, args, priority)
        with self.lock:
            self.processes[process.id] = process
            self.ready_queue.put((-priority, process.id))
        return process.id
    def start_process(self, process_id):
        with self.lock:
            if process_id in self.processes:
                process = self.processes[process_id]
                if process.state == "created":
                    process.start()
                    process.execution_count += 1
                    return True
        return False
    def terminate_process(self, process_id):
        with self.lock:
            if process_id in self.processes:
                self.processes[process_id].state = "terminated"
                del self.processes[process_id]
                return True
        return False
    def get_process_list(self):
        with self.lock:
            return [
                {
                    "id": p.id,
                    "name": p.name,
                    "state": p.state,
                    "priority": p.priority,
                    "executions": p.execution_count
                }
                for p in self.processes.values()
            ]
    def schedule_next(self):
        if not self.ready_queue.empty():
            _, process_id = self.ready_queue.get()
            self.start_process(process_id)
            return process_id
        return None