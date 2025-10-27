from datetime import datetime

class Metrics:
    def __init__(self):
        self.data = {"requests": 0, "errors": 0, "timestamp": str(datetime.now())}

    def record(self, key: str):
        if key in self.data:
            self.data[key] += 1
        self.data["timestamp"] = str(datetime.now())
