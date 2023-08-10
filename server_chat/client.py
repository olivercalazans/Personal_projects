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
            print('Registration completed')
        else:
            print(f'The name "{nameAndPassword[0]}" is not available')
    elif registerOrLogin == '1':
        nameAndPassword = (input('Name: '), input('Password: '))
        socketClient.send(str(nameAndPassword).encode())
        confirmation = socketClient.recv(BUFFER).decode()
        if confirmation == 'ok':
            print(f'Welcome, {nameAndPassword[0]}')
            break
        else:
            print('Name or password is wrong')
