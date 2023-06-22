import time
import random
from threading import Thread

class TransmitterData:
    def __init__(self, name, canal):
        self.name = name
        self.canal = canal
        self.retry_limit = 5

    def transmite(self, data):
        retry_count = 0
        while retry_count < self.retry_limit:
            if self.canal.is_idle():
                print(f"{self.name} está transmitindo:  {data}")
                if self.canal.transmit_data(data, self):
                    break
            else:
                print(f"{self.name} Aguardando........")
                self.canal.perform_backoff(retry_count)
                retry_count += 1

    def receive(self, data):
        print(f"{self.name} received: {data}")

class Canal:
    def __init__(self):
        self.transmitters = []
        self.transmitting = None

    def add_transmissor(self, transmitter):
        self.transmitters.append(transmitter)

    def is_idle(self):
        return self.transmitting is None

    def transmit_data(self, data, transmitter):
        self.transmitting = transmitter
        for receiver in self.transmitters:
            if receiver != transmitter:
                if self.detect_collision():
                    print("Colisão detectada!")
                    self.transmitting = None
                    return False
                receiver.receive(data)
        self.transmitting = None
        return True

    def detect_collision(self):
        collision_prob = 0.2  # Probability of collision
        return random.random() < collision_prob

    def perform_backoff(self, retry_count):
        max_backoff = 2 ** retry_count
        backoff_time = random.uniform(0, max_backoff)
        print(f"Aplicando backoff para {backoff_time} s. ")
        time.sleep(backoff_time)
