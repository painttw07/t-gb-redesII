import time
import random
#from threading import Thread

class TransmitterData:
    def __init__(self, name, canal):
        self.name = name
        self.canal = canal
        self.cont_limite = 5

    def transmite(self, data):
        cont_repeticao = 0
        while cont_repeticao < self.cont_limite:
            if self.canal.esta_livre():
                print(f"{self.name} \n--sensing the medium--")
                if self.canal.canal_livre():
                    print("LIVRE!!")
                    print(f"{self.name} transmitindo {data}")
                    if self.canal.transmite_dado(data, self):
                        break
                else:
                    print(f"{self.name} está OCUPADO!!!!")
                    self.canal.backoff(cont_repeticao)
                    cont_repeticao += 1
            else:
                print(f"{self.name} Aguardando.....")
                time.sleep(1)

    def recebe(self, data):
        print(f"{self.name} recebido: {data}")

class Canal:
    def __init__(self):
        self.transmitters = []
        self.transmitindo = None

    def add_transmissor(self, transmitter):
        self.transmitters.append(transmitter)

    def esta_livre(self):
        return self.transmitindo is None

    def canal_livre(self):
        for transmitter in self.transmitters:
            if transmitter != self.transmitindo:
                if not self.detector_colisao() and not self.detecta_ocupado():
                    return False
        return True

    def transmite_dado(self, data, transmitter):
        self.transmitindo = transmitter
        for recebedor in self.transmitters:
            if recebedor != transmitter:
                if self.detector_colisao():
                    print("Colisão detectada!")
                    self.transmitindo = None
                    return False
                recebedor.recebe(data)
        self.transmitindo = None
        return True

    def detecta_ocupado(self):
        ocupado_prob = 0.4  #probabilidade do canal estar ocupado
        return random.random() < ocupado_prob

    def detector_colisao(self):
        prob_colisao = 0.2  # Probabilidade de haver colisão
        return random.random() < prob_colisao

    def backoff(self, cont_repeticao):
        max_backoff = 2 ** cont_repeticao
        tempo_backoff = random.uniform(0, max_backoff)
        print(f"Backoff em {tempo_backoff} segundos. ")
        time.sleep(tempo_backoff)
