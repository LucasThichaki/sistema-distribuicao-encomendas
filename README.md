# Autores

<ul>
  <li>Kaio Henrique Gava Kiel</li>
  <li>Lucas Evangelista Thichaki</li>
  <li>Marcos Paulo Somera</li>
</ul> 

# Sistema de distribuição de encomendas

O sistema proposto busca realizar a simulação da distribuição de encomendas, com a utilização de conceitos de threads e semáforos para garantir exclusividade de acesso a cada ponto de distribuição. A quantidade de pontos, veículos, encomendas e a capacidade de carga dos veículos são definidas via input do usuário na inicialização do programa.

## Distribuição de classes

Foram pensados na divisão de 3 classes principais:

### Encomenda:

Com os atributos:
<ul>
  <li>ID</li>
  <li>Ponto de origem</li>
  <li>Ponto de destino</li>
  <li>Horário de origem</li>
  <li>Horário de carregamento</li>
  <li>Horário de destino</li>
  <li>Número de veículo</li>
</ul> 

### Veículo:

Com os atributos:
<ul>
  <li>ID</li>
  <li>Lista de cargas</li>
</ul> 

### Ponto de distribuição:

Com os atributos:
<ul>
  <li>ID</li>
  <li>Fila de encomendas</li>
</ul> 

## Funções

Para a realização das funcionalidades principais do sistema, foram utilizados 5 funções:

### cria_locks():

Utilizada para criar uma quantidade de semáforos (mutex) igual a quantidade de pontos de distribuição do sistema.

### cria_pontos():

Utilizada para inicialização de todos os pontos de distribuição do sistema e adiciona-los à lista circular de pontos.

### posiciona_encomenda():

Utilizada para inicializar todas as encomendas, sortear randomicamente os pontos de origem e destino e adiciona-la à lista de encomendas do seu ponto de distribuição de origem.

### cria_veiculos():

Utilizada para inicializar todos os veículos, sortear randomicamente seu ponto de origem e chamar a função, **movimenta_veiculo**, que irá despertar o movimento do veículo.

### movimenta_veiculo(veiculo, ponto):

Utilizada para definir o movimento de cada veículo pela lista de pontos, com tempos aleatórios de deslocamento, e realizar entrega e recebimento de encomendas.

<ul>
  <li>Entrega</li>
  Caso o veículo possua carga, todas as suas encomendas são verificadas, procurando alguma cujo o destino é o ponto atual. Ao encontrar, remove a encomenda do veículo, com tempo aleatório de descarregamento, e       cria o arquivo de rastro da encomenda em questão.
  <ul>
    <li>Arquivo de rastro:</li>
    Terá o ID da encomenda, sua origem e destino, seus horários de chegada na origem, carregamento e chegada no destino e o ID do veículo que realizou o transporte.
  </ul>
  
  <li>Recebimento</li>
  Enquanto existirem encomendas na fila do ponto de distribuição e o veículo tiver espaço de carga, a encomenda é removida da lista do ponto e carregada no veículo.
</ul> 

## Main

Na main, o sistema será inicializado com a atribuição dos valores principais definidos pelo usuário, e são inicializadas as diversas variáveis globais que serão utilizadas durante a execução. Para controlar a execução do programa, será atribuida uma variável **existe_encomenda** que controla a quantidade de encomendas que ainda não foram entregues, decrementando seu valor conforme entregas são realizadas e  encerrando a execução do programa caso seu valor se torne 0.

## Threads 

Foram definidas 3 blocos de criação de threads para cada uma das classes: Pontos, Encomendas e Veículos. Cada thread tem como alvo a função de inicialização da sua respectiva classe.

## Monitoramento dos dados

O sistema realiza a impressão, durante a sua execução, de mensagens de controle e monitoramento em situações específicas:

<ul>
  <li>Impressão do ID e do número de encomendas do ponto de distribuição no momento da chegada do veículo;</li>
  <li>Impressão do ID do veículo e do ponto de distribuição no momento da entrega da encomenda;</li>
  <li>Impressão do ID do veículo e da encomenda, ponto de origem e destino da encomenda e a capacidade atual de carga do veículo no momento em que o veículo recebe a encomenda;</li>
  <li>Impressão do ID do veículo no momento que ele sai do ponto de distribuição;</li>
  <li>Impressão do ID do veículo no momento de encerramento do sistema.</li>
</ul> 
