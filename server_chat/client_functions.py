import threading, sys

BUFFER = 1024
NAME   = ''

def tryingToCreateAnAccount(socketClient):
    nameAndPassword = (input('Write your name: '), input('Write a password: '))
    socketClient.send(str(nameAndPassword).encode())
    confirmation = socketClient.recv(BUFFER).decode()
    if confirmation == 'ok':
        print('\nRegistration completed')
    else:
        print(f'\nThe name "{nameAndPassword[0]}" is not available!!!')

def tryingToLogIn(socketClient):
    global NAME
    nameAndPassword = (input('Name: '), input('Password: '))
    socketClient.send(str(nameAndPassword).encode())
    confirmation = socketClient.recv(BUFFER).decode()
    if confirmation == 'ok':
        print(f'\nWelcome, {nameAndPassword[0]}')
        NAME = nameAndPassword[0]
        tRECEIVING_MESSAGES = threading.Thread(target=receivingMessagesFromTheServer, args=(socketClient,))
        tRECEIVING_MESSAGES.start()
        tSENDING_MESSAGES = threading.Thread(target=sendingMessagesToTheServer, args=(socketClient,))
        tSENDING_MESSAGES.start()
        return 'finished'
    else:
        print('\nName or password is wrong!!!')

def receivingMessagesFromTheServer(socketClient):
    while True:
        print(socketClient.recv(BUFFER).decode())
        
def sendingMessagesToTheServer(socketClient):
    while True:
        try:
            message = NAME + '> ' + input('')
            socketClient.send(message.encode())
        except:
            print(f'ERROR...:{sys.exc_info()}')
