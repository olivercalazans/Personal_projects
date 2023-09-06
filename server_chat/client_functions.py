

BUFFER = 1024

def tryingToCreateAnAccount(socketClient):
    nameAndPassword = (input('Write your name: '), input('Write a password: '))
    socketClient.send(str(nameAndPassword).encode())
    confirmation = socketClient.recv(BUFFER).decode()
    if confirmation == 'ok':
        print('\nRegistration completed')
    else:
        print(f'\nThe name "{nameAndPassword[0]}" is not available!!!')

def tryingToLogIn(socketClient):
    nameAndPassword = (input('Name: '), input('Password: '))
    socketClient.send(str(nameAndPassword).encode())
    confirmation = socketClient.recv(BUFFER).decode()
    if confirmation == 'ok':
        print(f'\nWelcome, {nameAndPassword[0]}')
        return 'finished'
    else:
        print('\nName or password is wrong!!!')