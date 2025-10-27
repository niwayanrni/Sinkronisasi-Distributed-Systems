import unittest
from src.nodes.lock_manager import LockManager

class TestLockManager(unittest.TestCase):
    def test_acquire_release(self):
        lm = LockManager()
        lock_id = "test_lock"
        self.assertTrue(lm.acquire(lock_id))
        self.assertFalse(lm.acquire(lock_id))
        lm.release(lock_id)
        self.assertTrue(lm.acquire(lock_id))

if __name__ == "__main__":
    unittest.main()