import unittest
import time
from fastapi.testclient import TestClient
from src.nodes.queue_node import app

class TestQueuePerformance(unittest.TestCase):
    def test_enqueue_performance(self):
        client = TestClient(app)
        start_time = time.time()
        for i in range(1000):
            response = client.post(
                "/enqueue",
                params={"key": f"user{i}"},
                json={"message": {"text": f"msg{i}"}}
            )
            self.assertEqual(response.status_code, 200)
        duration = time.time() - start_time
        print(f"[Queue] Enqueued 1,000 messages in {duration:.2f} seconds")
        self.assertLess(duration, 10, "Queue performance too slow")

if __name__ == "__main__":
    unittest.main()
