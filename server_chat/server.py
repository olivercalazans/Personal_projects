import sys, socket, threading, datetime
from server_functions import *

creatingFolders('\\HISTORY\\')
creatingFolders('\\CLIENTS\\')
creatingFiles('names_and_passwords.txt')
creatingFiles(str(datetime.date.today()))

try:
    socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketServer.bind(('0.0.0.0', 50000))
    socketServer.listen(5)
except: 
    print(f'\nERROR...:{sys.exc_info()}')
    HISTORY.append((str(datetime.datetime.now()), 'server activation', f'ERRO...:{sys.exc_info()}'))
    deactivating()
else:
    print('\nThe server is active\n')
    HISTORY.append((str(datetime.datetime.now()), 'server activation', 'sucessful activation'))

try:
    while True:
        connection, client = socketServer.accept()
        tREGISTER_LOGIN = threading.Thread(target=loggingInOrCreatingAnAccount, args=(connection, client,))
        tREGISTER_LOGIN.start()
        HISTORY.append((str(datetime.datetime.now()), 'connection', client))
except:
    print(f'\nERROR...:{sys.exc_info()}')
