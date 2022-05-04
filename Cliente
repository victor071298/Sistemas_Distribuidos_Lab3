# Mesmo cliente utilizado no lab2

import socket
import pickle

HOST = 'localhost' # maquina onde esta o servidor
PORTA = 5000        # porta que o servidor esta escutando

# cria socket
sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM 

# conecta-se com o servidor
sock.connect((HOST, PORTA)) 

msg = input("Digite o nome do arquivo\n")
sock.send(pickle.dumps(msg))
msg = pickle.loads(sock.recv(1024)) # argumento indica a qtde maxima de bytes da mensagem
    
# imprime a mensagem recebida
print(msg)

# encerra a conexao
sock.close
