class PBFTNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.state = "initial"
    
    def propose(self, request):
        pass
    
    def prepare(self, message):
        pass
    
    def commit(self, message):
        pass
