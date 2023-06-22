import time
import random
from threading import Thread

class TransmitterData: #classe que representa o funcionamento de um transmissor
    def __init__(self, name, canal):
        self.name = name
        self.canal = canal
        self.colidiu = False

    def transmite(self, data): #metodo tenta transmitir os dados como argumentos:
        #verifica se tem comunicação livre (esta_livre).abs
        #Se retornar true (está livre de fato) -> transmissão é feita atraves de transmite_dado
        #transmite_dado chama o método receive em cada transmissor conectado
        while True:
            if self.canal.esta_livre():
                print(f"{self.name} está transmitindo: {data}")
                self.canal.transmite_dado(data, self)
                break
            else:
                print(f"{self.name} Aguardando......")
                time.sleep(1)

    def receive(self, data):
        if self.colidiu:
            print(f"{self.name} está colidindo......")
            self.colidiu = False
        else:
            print(f"{self.name} está recebendo {data}")

    def detector_colisao(self):
            time.sleep(0.5)  # Simulating detection delay
            if self.canal.is_collision():
                print(f"{self.name} colisão detectada >.< ")
                self.colidiu = True

class Canal: #classe que representa o canal de comunicação que é compartilhado entre os transmissores 1 e 2
    def __init__(self):
        self.transmitters = [] #array de transmissores que estão ligados a classe Canal na L51 e L52        
        self.collision = False

    def add_transmissor(self, transmissor):
        self.transmitters.append(transmissor)

    def esta_livre(self):#verifica se algum dos transmissores está transmitindo no momento
    #simulando um tempo de transmissão
        for transmissor in self.transmitters:
            if transmissor != self:
                if self.transmitindo(transmissor):
                    print(" OCUPADO ")
                    return False 
        print(" LIVRE ")
        return True
        

    def is_collision(self):
        return self.collision

    def transmitindo(self, transmissor):
        # Simulating transmission time
        time.sleep(1)
        return random.choice([True, False])

    def transmite_dado(self, data, transmissor):
    #Inicia-se a thread para cada receptor (cada transmissor conectado, exceto o transmissor que está transmitindo)
    #e também uma thread separada para a detecção de colisões.
    #Em seguida, aguarda-se a conclusão de todas as threads antes de definir o status de colisão no canal.
        self.collision = False
        threads = []
        for recebedor in self.transmitters:
            if recebedor != transmissor:
                t = Thread(target=recebedor.receive, args=(data,))
                threads.append(t)
                t.start()

        # Start collision detection thread
        collision_thread = Thread(target=transmissor.detector_colisao)
        collision_thread.start()
        threads.append(collision_thread)

        # Wait for all threads to complete
        for t in threads:
            t.join()

        self.collision = any(transmissor.colidiu for transmissor in self.transmitters)

    def perform_backoff(self, retry_count): #nao ta funcionando essa porr*
        max_backoff = 2 ** retry_count
        backoff_time = random.uniform(0, max_backoff)
        print(f"Aplicando backoff para {backoff_time}segundos")
        time.sleep(backoff_time)
