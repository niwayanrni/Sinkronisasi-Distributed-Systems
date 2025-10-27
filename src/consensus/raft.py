import random
import threading
import time

class RaftNode:
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers
        self.state = "follower"
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_index = 0
        self.leader_id = None
        self.lock = threading.Lock()

    def request_vote(self):
        with self.lock:
            self.current_term += 1
            votes = 1
            for peer in self.peers:
                if random.random() > 0.5:
                    votes += 1
            if votes > len(self.peers) // 2:
                self.state = "leader"
                self.leader_id = self.node_id
                print(f"[RAFT] Node {self.node_id} elected as leader (term {self.current_term})")
            else:
                self.state = "follower"

    def append_entry(self, entry):
        with self.lock:
            self.log.append(entry)
            print(f"[RAFT] Node {self.node_id} appended entry: {entry}")

    def apply_log(self):
        if self.log:
            self.commit_index = len(self.log)
