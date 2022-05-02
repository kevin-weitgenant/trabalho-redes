from socket import *
from input_with_timeout import *

serverName=   '25.77.55.91'
serverPort=    77
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort)) 

message = ''
play = False
while(not play):

    message = clientSocket.recv(1024)
    message = message.decode('utf-8')
    
    if len(message) >0:
        print("message from server: ", message)
        if message.startswith('Numero sorteado'):
            play = True

game = True
while(game):
    
    message = clientSocket.recv(1500)
    message= message.decode("utf-8")
    
    if 'exit' in message:
        game = False

    else:    
        print("message from server: ", message)
        
        try:
            answer = input_with_timeout("O número está na lista(S/N)?", 3) 
        except TimeoutExpired:
            print('Tempo esgotado')
            print('Você não disse nada!')
            clientSocket.send(str.encode('0'))
        else:
            if answer == 'S':
                print('Você acredita que o numero está na lista!')
                clientSocket.send(str.encode('1'))
            elif answer == 'N':
                print('Você acredita que ele não está na lista!')
                clientSocket.send(str.encode('-1'))
            else:
                clientSocket.send(str.encode('0'))
                
        resultado1 = clientSocket.recv(1500)
        resultado2 = clientSocket.recv(1500)
        resultado1 = resultado1.decode("utf-8")
        resultado2 = resultado2.decode("utf-8")
        print(resultado1)
        print(resultado2)

result_final = clientSocket.recv(1500)
result_final = result_final.decode("utf-8")
print(result_final)
clientSocket.close()



