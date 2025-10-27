import unittest
import time
from fastapi.testclient import TestClient
from src.nodes.cache_node import app

class TestCachePerformance(unittest.TestCase):
    def test_set_get_performance(self):
        client = TestClient(app)
        start_time = time.time()
        for i in range(1000):
            set_res = client.post(f"/set?key=item{i}&value=value{i}")
            self.assertEqual(set_res.status_code, 200)

            get_res = client.get(f"/get?key=item{i}")
            self.assertEqual(get_res.status_code, 200)
        duration = time.time() - start_time
        print(f"[Cache] Set & retrieved 1,000 values in {duration:.2f} seconds")
        self.assertLess(duration, 15, "Cache performance too slow")

if __name__ == "__main__":
    unittest.main()
