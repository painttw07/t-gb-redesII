import time
import random
#from threading import Thread

class TransmitterData:
    def __init__(self, name, canal):
        self.name = name
        self.canal = canal
        self.cont_limite = 5 #limite da contagem

    def transmite(self, data):
        cont_repeticao = 0 #inicia as repetições em 0
        while cont_repeticao < self.cont_limite:
            if self.canal.esta_livre(): #se o meio estiver livre inicia o sensing, se ocupado, faz o backoff
                #se o meio está livre, começa a transmitir 
                print(f"{self.name} doing sensing")
                if self.canal.canal_livre():
                    print("CANAL LIVRE: ")
                    print(f"{self.name} transmitindo {data}")
                    if self.canal.transmite_dado(data, self):
                        break
                else:
                    print(f"{self.name} detectou canal ocupado!!")
                    self.canal.backoff(cont_repeticao)
                    cont_repeticao += 1
            else:
                print(f"{self.name} Aguardando.....") #se não fica em aguardando
                time.sleep(1)

    def recebe(self, data):
        print(f"{self.name} recebido: {data}") #recebimento do dado

class Canal:
    #inicial com array de transmissores e como transmitindo = 0 
    def __init__(self):
        self.transmitters = [] 
        self.transmitindo = None

    def add_transmissor(self, transmitter): #metodo de adição de transmissores
        self.transmitters.append(transmitter)

    def esta_livre(self):#nao está transmitindo
        return self.transmitindo is None 

    def canal_livre(self): #metodo que verifica quando o canal esta livre
        #ou seja, sem colisao ou não estando ocupado
        for transmitter in self.transmitters:
            if transmitter != self.transmitindo:
                if not self.detector_colisao() and not self.detecta_ocupado():
                    return False
        return True

    def transmite_dado(self, data, transmitter): #transmissao do dado em si
        self.transmitindo = transmitter
        for recebedor in self.transmitters:
            if recebedor != transmitter:
                if self.detector_colisao():
                    print("Colisão detectada!") #na detecção de colisão, nao transmite
                    self.transmitindo = None
                    return False
                recebedor.recebe(data) #se nao tiver colisao, transmite normal
        self.transmitindo = None
        return True

    def detector_colisao(self):
        prob_colisao = 0.2  # Probabilidade de haver colisão
        return random.random() < prob_colisao

    def detecta_ocupado(self):
        ocupado_prob = 0.4  #probabilidade do canal estar ocupado
        return random.random() < ocupado_prob

    def backoff(self, cont_repeticao): #tentativa de metodo pra backoff
        max_backoff = 1 ** cont_repeticao #calculo do ''valor maximo de backoff''
        tempo_backoff = random.uniform(0, max_backoff)
        print(f"Backoff em {tempo_backoff} segundos. ")
        time.sleep(tempo_backoff)
