import sys, socket, threading
from functions import *

creatingFoldersAndFile('\\HISTORY\\')
creatingFoldersAndFile('\\CLIENTS\\')
creatingFoldersAndFile('names_and_passwords.txt')

try:
    socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketServer.bind(('0.0.0.0', 50000))
    socketServer.listen(5)
except: 
    print(f'\nERRO...:{sys.exc_info()}')
    HISTORY.append((TODAYS_DATE, 'server activation', f'ERRO...:{sys.exc_info()}'))
    deactivating()
else:
    print('\nThe server is active\n')
    HISTORY.append((TODAYS_DATE, 'server activation', 'sucessful activation'))

try:
    while True:
        connection, client = socketServer.accept()
        tREGISTER_LOGIN = threading.Thread(target=loggingInOrCreatingAnAccount, args=(connection, client,))
        tREGISTER_LOGIN.start()
        HISTORY.append((TODAYS_DATE, 'connection', client))
except:
    print(f'\nERROR...:{sys.exc_info()}')
