class PBFTNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.state = "initial"
    
    def propose(self, request):
        # logic for proposing a request
        pass
    
    def prepare(self, message):
        # logic for prepare phase
        pass
    
    def commit(self, message):
        # logic for commit phase
        pass
