import datetime, os, sys, socket, threading


# ============================================ CONSTANTS =================================================

ALL_CLIENTS = list()
HISTORY     = list()
BUFFER      = 1024
TODAYS_DATE = str(datetime.date.today())
DIRECTORY   = os.path.dirname(os.path.abspath(__file__))

# ============================================ FUNCTIONS =================================================

def creating_folder(folderName):
    try:    os.mkdir(DIRECTORY + folderName)
    except  FileExistsError: print('The folder already exists')
    except: print(f'\nERRO...:{sys.exc_info()[0]}')
    else:   print('The folder was created')

def writing_history():
    ...

def register_login(connection, client):
    while True:
        registerOrLogin = connection.recv(BUFFER).decode()
        # Registration
        if registerOrLogin == '0':
            while True:
                nameAndPassword = connection.recv(BUFFER).decode()



# ========================================================================================================

print('\nCreating folder for history')
creating_folder('\\HISTORY\\')

print('Creating folder for clients')
creating_folder('\\CLIENTS\\')

try:
    socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketServer.bind(('0.0.0.0', 50000))
    socketServer.listen(5)
except: 
    print(f'\nERRO...:{sys.exc_info()}')
    sys.exit()
else: print('\nThe server is active\n')

try:
    while True:
        connection, client = socketServer.accept()
        tREGISTER_LOGIN = threading.Thread(target=register_login, args=(connection, client,))
        tREGISTER_LOGIN.start()
        HISTORY.append((TODAYS_DATE, 'connection', client))
except:
    print(f'\nERRO...:{sys.exc_info()}')
    
