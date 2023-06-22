import random
import time
from transmissores import TransmitterData, Canal

# Criando o meio de comunicação
canal = Canal()

# Criando os transmissores
t1 = TransmitterData("Transmissor 1", canal)
t2 = TransmitterData("Transmissor 2", canal)
t3 = TransmitterData("Transmissor 3", canal)


# Adicionando os transmissores ao meio de comunicação
canal.add_transmissor(t1)
canal.add_transmissor(t2)
canal.add_transmissor(t3)

# Testando a transmissão de dados
t1.transmite("Bom dia do Transmissor 1!")
t2.transmite("Boa noite do Transmissor 2!!!!!!")
t3.transmite("aaaaaaaaaaaaaa")

print("\n FIM! *-* ")
