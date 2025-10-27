from src.consensus.raft import RaftNode

class LockManager:
    def __init__(self, node_id, peers):
        self.raft = RaftNode(node_id, peers)
        self.locks = {}

    def acquire_lock(self, resource_id, node_id, lock_type="exclusive"):
        if self.raft.state != "leader":
            print(f"[LOCK] Node {self.raft.node_id} bukan leader, tidak bisa kunci langsung.")
            return False

        if resource_id not in self.locks:
            self.locks[resource_id] = {"type": lock_type, "holders": {node_id}}
            self.raft.append_entry((resource_id, lock_type, node_id))
            print(f"[LOCK] {node_id} acquired {lock_type} lock on {resource_id}")
            return True

        existing = self.locks[resource_id]
        if lock_type == "shared" and existing["type"] == "shared":
            existing["holders"].add(node_id)
            self.raft.append_entry((resource_id, lock_type, node_id))
            return True
        else:
            print(f"[LOCK] {resource_id} sudah dikunci secara {existing['type']}")
            return False

    def release_lock(self, resource_id, node_id):
        if resource_id in self.locks and node_id in self.locks[resource_id]["holders"]:
            self.locks[resource_id]["holders"].remove(node_id)
            if not self.locks[resource_id]["holders"]:
                del self.locks[resource_id]
            print(f"[LOCK] {node_id} released lock on {resource_id}")
            return True
        return False
