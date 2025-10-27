class CacheNode(base_node):
    def __init__(self, node_id: str):
        super().__init__(node_id)
        self.cache = {}

    def read(self, key: str):
        """Read from cache"""
        pass

    def write(self, key: str, value: dict):
        """Write to cache"""
        pass

    def invalidate(self, key: str):
        """Invalidate cache entry"""
        pass
