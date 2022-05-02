from random import randint
import socket
from time import sleep, time
serverPort = 77
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
from _thread import *

try:
	serverSocket.bind(('25.77.55.91',serverPort))
except socket.error as e:
	print("Erro ao criar o socket: ", e)
	exit()
		
serverSocket.listen(2)
print ("Server is ready to receive")



player = 0
game = True
connectionArr = []
addrArr = []
MAX_POINTS = 3

while player<2:
	connectionSocket, addr = serverSocket.accept()
	
	connectionArr.append(connectionSocket)
	addrArr.append(addr)
	
	print("Conexão estabelecida com: ", addr)
	connectionArr[player].send(str.encode(f"Bem vindo ao jogo player {player+1}"))
	player+=1
	if player == 1:
		connectionArr[0].send(str.encode(f"Aguardando o player 2"))
	
connectionArr[0].send(str.encode(f"Player 2 chegou, vamos comecar",'utf-8'))

while game:
	numero = randint(0,20)

	
	connectionArr[0].send(str.encode(f"Numero sorteado: {numero}"))
	connectionArr[1].send(str.encode(f"Numero sorteado: {numero}"))
	sleep(4)

	reply1 = ""
	reply2 = ""
	p1_points = 0
	p2_points = 0

	while p1_points != MAX_POINTS and p2_points != MAX_POINTS:
		
		numeros = [randint(0,20) for quantidade in range(10)]
		existe = 1 if numero in numeros else -1
		
		
		numeros = " ".join([str(item) for item in numeros])
		connectionArr[0].send(str.encode(f"{numeros}"))
		connectionArr[1].send(str.encode(f"{numeros}"))
		sleep(1)

		reply1 = int(connectionArr[0].recv(1024).decode('utf-8'))
		reply2 = int(connectionArr[1].recv(1024).decode('utf-8'))

		p1_rodada = existe * reply1
		p2_rodada = existe * reply2
		dicionario = {1:">>>> Acertou",-1:">>>> Errou",0:">>>> Não respondeu"}
		p1_points+= p1_rodada
		p2_points+= p2_rodada

		connectionArr[0].send(str.encode(f"{dicionario[p1_rodada]}\n"))
		connectionArr[0].send(str.encode(f"\nSua pontuação:\t{p1_points}\n"))
		connectionArr[1].send(str.encode(f"\nSua pontuação:\t{p2_points}\n"))
		connectionArr[1].send(str.encode(f"{dicionario[p2_rodada]}\n"))
		
		sleep(2)
	game = False

connectionArr[0].send(str.encode(f"exit"))
connectionArr[1].send(str.encode(f"exit"))

if p1_points == MAX_POINTS:
	connectionArr[0].send(str.encode(f"Você ganhou!"))
	connectionArr[1].send(str.encode(f"Você perdeu!"))
elif p2_points == MAX_POINTS:
	connectionArr[0].send(str.encode(f"Você perdeu!"))
	connectionArr[1].send(str.encode(f"Você ganhou!"))
