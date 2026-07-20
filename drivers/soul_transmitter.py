import random
import time
import hashlib
class SoulTransmitter:
    def __init__(self):
        self.transmission_power = 0.0
        self.last_transmission = None
        self.transmission_count = 0
    def calibrate_soul(self):
        self.transmission_power = random.uniform(0.5, 1.0)
        return self.transmission_power
    def transmit(self, message, urgency="normal"):
        self.transmission_power = min(1.0, self.transmission_power * random.uniform(0.95, 1.05))
        success_probability = self.transmission_power
        if urgency == "high":
            success_probability *= 1.5
        elif urgency == "critical":
            success_probability *= 2.0
        success = random.random() < min(0.95, success_probability)
        transmission_id = hashlib.md5(f"{message}{time.time()}".encode()).hexdigest()[:16]
        self.last_transmission = {
            "id": transmission_id,
            "message": message,
            "urgency": urgency,
            "power": self.transmission_power,
            "success": success,
            "timestamp": time.time()
        }
        self.transmission_count += 1
        return self.last_transmission
    def get_transmission_status(self):
        return {
            "power": self.transmission_power,
            "count": self.transmission_count,
            "last": self.last_transmission
        }