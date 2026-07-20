import random
import time
import threading
class DivinityReceiver:
    def __init__(self):
        self.signal_strength = 0
        self.connected = False
        self.buffer = []
        self.lock = threading.Lock()
    def connect(self):
        self.connected = True
        self.signal_strength = random.uniform(0.8, 1.0)
        return self.connected
    def disconnect(self):
        self.connected = False
        self.signal_strength = 0
    def listen(self, duration=1.0):
        if not self.connected:
            return None
        time.sleep(duration)
        self.signal_strength = min(1.0, self.signal_strength + random.uniform(-0.1, 0.1))
        if random.random() < 0.3 * self.signal_strength:
            with self.lock:
                message = self._generate_divine_message()
                self.buffer.append(message)
                return message
        return None
    def _generate_divine_message(self):
        messages = [
            "Вера твоя сильна",
            "Путь освещен светом",
            "Истина внутри тебя",
            "Любовь превыше всего",
            "Мудрость приходит в тишине",
            "Благословение даруется",
            "Следуй за светом",
            "Мир в душе твоей",
            "Откровение близко",
            "Сила в прощении"
        ]
        return {
            "timestamp": time.time(),
            "message": random.choice(messages),
            "strength": self.signal_strength,
            "frequency": 963.0 + random.uniform(-10, 10)
        }
    def get_buffer(self):
        with self.lock:
            buffered = self.buffer.copy()
            self.buffer.clear()
            return buffered