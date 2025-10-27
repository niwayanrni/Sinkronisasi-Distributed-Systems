import threading
from typing import Any, Dict

class MessageBus:
    """In-memory message passing dengan support network partition"""
    def __init__(self):
        self.subscribers: Dict[str, list] = {}
        self.lock = threading.Lock()
        self.partitions = set()

    def subscribe(self, topic: str, subscriber_id: str, callback):
        """Daftarkan subscriber ke topic"""
        with self.lock:
            if topic not in self.subscribers:
                self.subscribers[topic] = []
            self.subscribers[topic].append((subscriber_id, callback))

    def publish(self, topic: str, sender: str, msg_id: str, payload: Any):
        """Publish message ke semua subscriber di topic, kecuali kalau partition"""
        with self.lock:
            if topic in self.subscribers:
                for subscriber_id, cb in self.subscribers[topic]:
                    if (sender, subscriber_id) in self.partitions:
                        print(f"[NET] Partition between {sender} and {subscriber_id}, message dropped.")
                        continue
                    threading.Thread(target=cb, args=(msg_id, payload)).start()
                    print(f"[NET] {sender} -> {subscriber_id}: {msg_id}")

    def add_partition(self, a: str, b: str):
        self.partitions.add((a, b))
        self.partitions.add((b, a))
        print(f"[NET] Partition added between {a} and {b}")

    def remove_partition(self, a: str, b: str):
        self.partitions.discard((a, b))
        self.partitions.discard((b, a))
        print(f"[NET] Partition removed between {a} and {b}")
