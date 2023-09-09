import socket, sys
from client_functions import *

try:
    socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketClient.connect(('localhost', 50000))
except:
    print(f'\nERROR...:{sys.exc_info()}')
    sys.exit()
else:
    print('\nConnected to the server')

while True:
    try:
        registerOrLogin = input('\n0 - Register\n1 - Login\nWrite the number: ')
        socketClient.send(registerOrLogin.encode())
        if registerOrLogin == '0':
            tryingToCreateAnAccount(socketClient)
        elif registerOrLogin == '1':
            confirmation = tryingToLogIn(socketClient)
            if confirmation == 'finished': break
    except KeyboardInterrupt:
        print('Disconnecting from the server')
        socketClient.send('force')
        break
    except:
        ...
