import unittest
from src.nodes.queue_node import QueueNode

class TestDistributedQueueIntegration(unittest.TestCase):
    def setUp(self):
        self.node1 = QueueNode("node1")
        self.node2 = QueueNode("node2")

    def test_enqueue_dequeue_across_nodes(self):
        self.node1.enqueue("task1")
        item = self.node2.dequeue()
        self.assertEqual(item, "task1")

if __name__ == "__main__":
    unittest.main()
