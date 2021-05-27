import time
from socket import *


host = str(input("Enter server address: "))
port = 1234

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((host, port))

print('Waiting for the connection...')

client_name = input('Enter your name:')
client_socket.send(client_name.encode())
server_name = client_socket.recv(1024)
server_name = server_name.decode()
print(server_name, 'is ready!')

words = []

server_message = client_socket.recv(1024)
server_message = server_message.decode()
words.append(server_message)
print(f'{server_name}: {server_message}')

time_left = 20
while True:

    start_time = time.time()
    client_message = input("Enter your word:")

    if client_message == 'exit':
        message = client_name + " left the game!"
        print(message)
        client_socket.send(message.encode())
        break

    elif server_message[-2:] != client_message[0:2]:
        print("The word must start with ", server_message[-2:])
        time_spent = time.time() - start_time
        time_left = time_left - time_spent
        continue

    elif client_message in words:
        print("The word you entered has already been used, try again!")
        time_spent = time.time() - start_time
        time_left = time_left - time_spent
        continue

    else:
        time_spent = time.time() - start_time
        time_left = time_left - time_spent
        if time_left <= 0:
            print("time is up", server_name, "won!")
            message = "Time is up! You won!"
            client_socket.send(message.encode())
            break
        client_socket.send(client_message.encode())
        words.append(client_message)

    server_message = client_socket.recv(1024)
    server_message = server_message.decode()
    exit_msg = server_name + " left the game!"
    if (server_message == 'Time is up! You won!') or (server_message == exit_msg):
        print(server_message)
        break
    words.append(server_message)
    print(f'{server_name}: {server_message}')
    time_left = 20
