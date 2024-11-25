import threading
import time
import random

#Classes--------------------------------------------------------------------------------------------------------------------

class Encomenda:
    def __init__(self, id, origem, destino, horario_origem, horario_carregamento = 0, num_veiculo = 0, horario_destino = 0):
        self.id = id
        self.origem = origem
        self.destino = destino
        self.horario_origem = horario_origem
        self.horario_carregamento = horario_carregamento
        self.num_veiculo = num_veiculo
        self.horario_destino = horario_destino


class Veiculo:
    def __init__(self, id, carga):
        self.id = id
        self.carga = carga


class Ponto_Distribuicao:
    def __init__(self, id, encomendas):
        self.id = id
        self.encomendas = encomendas


#Funções------------------------------------------------------------------------------------------------------------------------


def cria_locks():
    global n_pontos_distribuicao, lista_mutex
    for i in range(n_pontos_distribuicao):
        mutex = threading.Lock()
        lista_mutex.append(mutex)


def cria_pontos():
    global id_pontos, lista_de_pontos
    ponto_distribuicao = Ponto_Distribuicao(id = id_pontos, encomendas = [])
    id_pontos += 1
    lista_de_pontos.append(ponto_distribuicao)


def posiciona_encomenda():
    global n_encomendas, n_pontos_distribuicao, id_encomendas
    encomenda = Encomenda(id = id_encomendas, origem = random.randint(0,n_pontos_distribuicao-1), destino = random.randint(0,n_pontos_distribuicao-1), horario_origem = time.time() - tempo_inicio)
    id_encomendas += 1
    lista_de_pontos[encomenda.origem].encomendas.append(encomenda)


def cria_veiculos():
    global id_veiculos, n_pontos_distribuicao
    veiculo = Veiculo(id = id_veiculos, carga = [])
    id_veiculos += 1
    ponto_de_origem = random.randint(0,n_pontos_distribuicao-1)
    movimenta_veiculo(veiculo, ponto_de_origem)


def movimenta_veiculo(veiculo, ponto):
    global capacidade_veiculo, lista_de_pontos, lista_mutex, existe_encomenda, n_pontos_distribuicao, tempo_inicio
    while existe_encomenda:
        lista_mutex[ponto].acquire()
        print('Veículo', veiculo.id, 'chegou no ponto', ponto, '(Há', len(lista_de_pontos[ponto].encomendas), 'encomendas nesse ponto)')
        #Entrega encomenda:
        if len(veiculo.carga) > 0:
            pos = 0
            removidos = 0
            for encomenda in veiculo.carga:
                if encomenda.destino == ponto:
                    #Descarrega a encomenda
                    descarregada = veiculo.carga.pop(pos - removidos)
                    removidos += 1
                    tempo_descarregamento = random.randint(200,2000)
                    time.sleep(tempo_descarregamento/1000)
                    existe_encomenda -= 1
                    descarregada.horario_destino = time.time() - tempo_inicio
                    print('Veiculo', veiculo.id, 'entregou a encomenda', descarregada.id, 'no ponto', ponto)
                    arquivo = f'rastro_encomenda{descarregada.id}.txt'
                    fp = open(arquivo,'w')
                    fp.write(f'Numero da encomenda:{descarregada.id}\n origem:{descarregada.origem}\n destino:{descarregada.destino}\n horario de chegada na origem:{round(descarregada.horario_origem, 2)}s\n horario de carregamento:{round(descarregada.horario_carregamento, 2)}s\n veiculo que realizou o transporte:{veiculo.id}\n horario de descarregamento:{round(descarregada.horario_destino,2)}s')
                    fp.close()
                pos += 1
        #Recebe encomenda:
        while len(lista_de_pontos[ponto].encomendas) > 0:
            if len(veiculo.carga) < capacidade_veiculo:
                nova_encomenda = lista_de_pontos[ponto].encomendas.pop(0)
                print('Veiculo', veiculo.id, 'recebeu a encomenda:', nova_encomenda.id, '( Origem: ponto', ponto, '/ Destino: ponto', nova_encomenda.destino, ')')
                veiculo.carga.append(nova_encomenda)
                print('Capacidade do veiculo', veiculo.id, '=', len(veiculo.carga), '/', capacidade_veiculo)
                nova_encomenda.horario_carregamento = time.time() - tempo_inicio
                nova_encomenda.num_veiculo = veiculo.id
            else:
                break
        print('Veiculo', veiculo.id, 'saiu do ponto', ponto)
        lista_mutex[ponto].release()
        
        ponto = (1 + ponto) % n_pontos_distribuicao
        tempo_deslocamento = random.randint(200,2000)
        time.sleep(tempo_deslocamento/1000)
    print('Veiculo', veiculo.id, 'encerrou')


#Main---------------------------------------------------------------------------------------------------------------------------------------

print('Sistema de Distribuição de Encomendas\n--------------------------------------\nInsira os dados do sistema:\n')

n_encomendas = int(input('Insira o número de encomendas: '))
n_veiculos = int(input('Insira o número de veículos: '))
n_pontos_distribuicao = int(input('Insira o número de pontos de distribuição: '))
capacidade_veiculo = int(input('Insira a capacidade de cada veículo: '))
print('\n\n')

tempo_inicio = time.time()
lista_mutex = []

id_encomendas = 0
id_veiculos = 0
id_pontos = 0

lista_de_pontos = []

existe_encomenda = n_encomendas

cria_locks()


#Threads----------------------------------------------------------------------------------------------------------------------------------

threads_p = []
for i in range(n_pontos_distribuicao):
    thread = threading.Thread(target=cria_pontos)
    threads_p.append(thread)
    thread.start()

threads_e = []
for i in range(n_encomendas):
    thread = threading.Thread(target=posiciona_encomenda)
    threads_e.append(thread)
    thread.start()

threads_v = []
for i in range(n_veiculos):
    thread = threading.Thread(target=cria_veiculos)
    threads_v.append(thread)
    thread.start()

for thread in threads_p:
    thread.join()

for thread in threads_e:
    thread.join()

for thread in threads_v:
    thread.join()
