class BaseNode:
    def __init__(self, node_id: str):
        self.node_id = node_id

    def start(self):
        """Start node service"""
        pass

    def stop(self):
        """Stop node service"""
        pass
