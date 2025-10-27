import hashlib
import threading
import queue
import sqlite3
import pickle
import os
from typing import Any, Dict, List

class QueueNode:
    def __init__(self, node_id: str, db_path: str = "queue_db.sqlite"):
        self.node_id = node_id
        self.queue = queue.Queue()
        self.lock = threading.Lock()
        self.db_path = db_path
        self._setup_db()
    
    def _setup_db(self):
        """Buat tabel message persistence jika belum ada"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                payload BLOB
            )
        """)
        conn.commit()
        conn.close()

    def persist_message(self, msg_id: str, payload: Any):
        """Simpan pesan ke database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO messages (id, payload) VALUES (?, ?)",
                  (msg_id, pickle.dumps(payload)))
        conn.commit()
        conn.close()

    def recover_messages(self):
        """Load pesan yang belum dikonsumsi dari database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT id, payload FROM messages")
        rows = c.fetchall()
        for msg_id, payload_blob in rows:
            payload = pickle.loads(payload_blob)
            self.queue.put((msg_id, payload))
        conn.close()

    def add_message(self, msg_id: str, payload: Any):
        """Add message ke queue + persist"""
        with self.lock:
            self.persist_message(msg_id, payload)
            self.queue.put((msg_id, payload))

    def consume_message(self):
        """Ambil message dari queue"""
        try:
            msg_id, payload = self.queue.get(timeout=1)
            return msg_id, payload
        except queue.Empty:
            return None, None

class ConsistentHashRing:
    def __init__(self, nodes: List[str]):
        self.ring = sorted([(self.hash_key(n), n) for n in nodes])

    @staticmethod
    def hash_key(key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def get_node(self, key: str) -> str:
        h = self.hash_key(key)
        for node_hash, node_id in self.ring:
            if h <= node_hash:
                return node_id
        return self.ring[0][1]  # Wrap around
