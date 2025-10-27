import unittest
from fastapi.testclient import TestClient
from src.nodes.lock_manager import app
import time

class TestLockPerformanceAPI(unittest.TestCase):
    def test_lock_unlock_performance(self):
        client = TestClient(app)
        start = time.time()
        for i in range(1000):

            r1 = client.post("/lock/acquire", params={"resource_id": f"res{i}"})
            self.assertEqual(r1.status_code, 200)

            r2 = client.post("/lock/release", params={"resource_id": f"res{i}"})
            self.assertEqual(r2.status_code, 200)
        end = time.time()
        print(f"[LOCK] 1000 lock/unlock ops in {end - start:.2f} s")
        self.assertLess(end - start, 15, "Lock performance too slow")

if __name__ == "__main__":
    unittest.main()
