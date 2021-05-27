import socket
import time
import sys

print('Welcome to the game!')

port = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(socket.gethostname())
server_socket.bind((socket.gethostname(), port))
server_socket.listen(2)
connection, add = server_socket.accept()

server_name = input('Please enter your name:')

client_name = connection.recv(1024)
client_name = client_name.decode()
print(client_name, "is ready!")
connection.send(server_name.encode())

words = []

while True:
    server_message = input('Enter the first word:')
    if len(server_message)>1:
        connection.send(server_message.encode())
        words.append(server_message)
        break
    print("Your word should contain at least 2 characters.")

client_message = connection.recv(1024)
client_message = client_message.decode()
exit_msg = client_name + " left the game!"
if (client_message == 'Time is up! You won!') or (client_message == exit_msg):
    print(client_message)
    sys.exit()
words.append(client_message)
print(f'{client_name}: {client_message}')

time_left = 20
while True:

    start_time = time.time()
    server_message = input('Enter your word:')

    if server_message == 'exit':
        message = server_name + " left the game!"
        print(message)
        connection.send(message.encode())
        break
    elif client_message[-2:] != server_message[0:2]:
        print("The word must start with ", client_message[-2:])
        time_spent = time.time() - start_time
        time_left = time_left - time_spent
        continue
    elif server_message in words:
        print("The word you entered has already been used, try again!")
        time_spent = time.time() - start_time
        time_left = time_left - time_spent
        continue
    else:
        time_spent = time.time() - start_time
        time_left = time_left - time_spent
        if time_left <= 0:
            print("time is up", client_name, "won!")
            message = "Time is up! You won!"
            connection.send(message.encode())
            break
        connection.send(server_message.encode())
        words.append(server_message)

    client_message = connection.recv(1024)
    client_message = client_message.decode()
    exit_msg = client_name + " left the game!"
    if (client_message == 'Time is up! You won!') or (client_message == exit_msg):
        print(client_message)
        break
    words.append(client_message)
    print(f'{client_name}: {client_message}')

    time_left = 20





