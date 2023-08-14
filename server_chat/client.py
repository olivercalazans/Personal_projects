import socket

# =================================== CONSTANTS ==================================
BUFFER = 1024
# ================================================================================

socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketClient.connect(('localhost', 50000))

while True:
    registerOrLogin = input('\n0 - Register\n1 - Login\nWrite the number: ')
    socketClient.send(registerOrLogin.encode())
    if registerOrLogin == '0':
        nameAndPassword = (input('Write your name: '), input('Write a password: '))
        socketClient.send(str(nameAndPassword).encode())
        confirmation = socketClient.recv(BUFFER).decode()
        if confirmation == 'ok':
            print('\nRegistration completed')
        else:
            print(f'\nThe name "{nameAndPassword[0]}" is not available!!!')
    elif registerOrLogin == '1':
        nameAndPassword = (input('Name: '), input('Password: '))
        socketClient.send(str(nameAndPassword).encode())
        confirmation = socketClient.recv(BUFFER).decode()
        if confirmation == 'ok':
            print(f'\nWelcome, {nameAndPassword[0]}')
            break
        else:
            print('\nName or password is wrong!!!')
