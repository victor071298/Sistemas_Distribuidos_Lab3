import os
import socket
import pickle
import select 
import multiprocessing
import sys

#define a lista de I/O de interesse (jah inclui a entrada padrao)
entradas = [sys.stdin]
#armazena historico de conexoes
conexoes = {}

def top5(nome_do_arquivo):

    # dicionário vazio que armazenará as palavras e a quantidade de vezes que elas aparecem
    palavra_quantidade = {}
    # Checando se o arquivo existe
    if os.path.exists(nome_do_arquivo + '.txt'): #o path deve ser modificado dependendo de onde se encontra o arquivo na máquina do servidor
        with open(nome_do_arquivo + '.txt') as arquivo:
            for linha in arquivo.readlines():
                for palavra in linha.split(' '):
                    if palavra in palavra_quantidade:
                        palavra_quantidade[palavra] += 1
                    else:
                        palavra_quantidade[palavra] = 1
    else:
        print("Erro, arquivo não encontrado")
        falha = "O arquivo enviado não foi encontrado"
        return falha

    # Encontrando as 5 palavras mais frequentes
    palavras_mais_frequentes = []
    for i in range(5):
        maior_palavra = None # palavra mais encontrada
        maior_valor = 0 # contador da maior palavra

        for palavra, contagem in palavra_quantidade.items():
            if contagem > maior_valor:
                maior_palavra = palavra
                maior_valor = contagem

        palavras_mais_frequentes.append(maior_palavra)
        del palavra_quantidade[maior_palavra]

    # retornando as palavras encontradas
    return palavras_mais_frequentes

#Funcao responsavel por atender as requisicoes do cliente
def atendeRequisicao(clisock,endr):
    data = pickle.loads(clisock.recv(1024))
    envio = top5(data) # encontrando os 5 elementos mais comuns
    print(envio)
    
    clisock.send(pickle.dumps(envio)) # enviando o resultado encontrado para o cliente
    
    # fecha o socket da conexão
    clisock.close()
    
    #retirando cliente da lista de conexoes
    del conexoes[clisock]
    
# Início do servidor

HOST = ''    # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORTA = 5000  # porta onde chegarao as mensagens para essa aplicacao

# armazena todos os clientes para fazer um join
clientes = []

# cria um socket para comunicacao
sock = socket.socket() # valores default: socket.AF_INET, socket.SOCK_STREAM  

# vincula a interface e porta para comunicacao
sock.bind((HOST, PORTA))

# define o limite maximo de conexoes pendentes e coloca-se em modo de espera por conexao
sock.listen(5)

entradas.append(sock)

sock.setblocking(False)

while True:
    leitura, escrita, excecao = select.select(entradas,[],[])
    for pronto in leitura:
        if pronto == sock:
            clisock, endr = sock.accept()
            print ('Conectado com: ', endr)
            conexoes[clisock] = endr
            cliente = multiprocessing.Process(target=atendeRequisicao, args=(clisock,endr))
            cliente.start()
            clientes.append(cliente) #armazena a referencia da thread para usar com join() 
        elif pronto == sys.stdin: 
            cmd = input()
            if cmd == 'fim': #solicitacao de finalizacao do servidor
                for c in clientes: #aguarda todos os processos terminarem
                    c.join()
                sock.close() #encerrando a conexão
                sys.exit() #encerrando o programa
 
