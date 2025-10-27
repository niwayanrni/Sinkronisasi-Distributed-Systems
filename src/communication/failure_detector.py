import time

class FailureDetector:
    def __init__(self, nodes, timeout=5):
        self.nodes = nodes
        self.timeout = timeout
        self.last_seen = {node: time.time() for node in nodes}

    def heartbeat(self, node):
        self.last_seen[node] = time.time()

    def check_failures(self):
        current_time = time.time()
        failed_nodes = [node for node, ts in self.last_seen.items() if current_time - ts > self.timeout]
        return failed_nodes
