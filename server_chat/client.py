import socket

# =================================== CONSTANTS ==================================

BUFFER = 1024

# ================================================================================

socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketClient.connect(('localhost', 50000))

while True:
    registerOrLogin = input('0 - Register\n1 - Login\nWrite the number: ')
    socketClient.send(registerOrLogin.encode())
    if registerOrLogin == '0':
        while True:
            nameAndPassword = str((input('Write your name: '), input('Write a password: ')))
            socketClient.send(nameAndPassword.encode())
            confirmation = socketClient.recv(BUFFER).decode()
            if confirmation == 'ok':
                print('Registration completed')
                break
            else:
                print(f'The name {nameAndPassword[0]} is not available')
    elif registerOrLogin == '1':
        while True:
            nameAndPassword = str((input('Name: '), input('Password: ')))
            socketClient.send(nameAndPassword.encode())
            confirmation = socketClient.recv(BUFFER).decode()
            if confirmation == 'ok':
                break
            else:
                print('Name or password is wrong')

        
   

