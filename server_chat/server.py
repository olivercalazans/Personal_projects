import datetime, os, sys, socket, threading

# ============================================ CONSTANTS =================================================
NAMES_AND_PASSWORDS = list()
ONLINE_CLIENTS      = list()
HISTORY             = list()
BUFFER              = 1024
TODAYS_DATE         = str(datetime.date.today())
DIRECTORY           = os.path.dirname(os.path.abspath(__file__))
# ============================================ FUNCTIONS =================================================

# Function for the creation of important folders and file.
def creating_folder(folderName):
    try: 
        print(f'##Creating "{folderName}"##')
        if folderName == 'names_and_passwords.txt':
            if os.path.exists(DIRECTORY + '\\CLIENTS\\' + folderName): raise FileExistsError
            else:
                with open(DIRECTORY + '\\CLIENTS\\' + folderName, 'w'): pass
        else: os.mkdir(DIRECTORY + folderName)
    except FileExistsError: 
        print(f'"{folderName}" already exists')
        HISTORY.append((TODAYS_DATE, f'creating {folderName}', 'FileExistsError'))
    except: 
        print(f'\nERRO...:{sys.exc_info()[0]}')
        HISTORY.append((TODAYS_DATE, f'creating {folderName}', {sys.exc_info()[0]}))
    else:
        print(f'"{folderName}" was created')
        HISTORY.append((TODAYS_DATE, f'creating {folderName}', 'Successfully created'))

# Writing history
def writing_history():
    with open(DIRECTORY + '\\CLIENT\\' + 'names_and_passwords.txt', 'w', encoding='utf-8') as pen:
        for line in HISTORY: pen.write(line)
        HISTORY = list()

# Creating a new account or logging in
def register_login(connection, client):
    while True:
        registerOrLogin = connection.recv(BUFFER).decode()
        # Registration
        if registerOrLogin == '0':
            nameAndPassword = connection.recv(BUFFER).decode()
            if nameAndPassword in NAMES_AND_PASSWORDS:
                connection.send('wrong'.encode())
                HISTORY.append((TODAYS_DATE, 'creating account', 'name unavailable', client))
            else: 
                NAMES_AND_PASSWORDS.append(nameAndPassword)
                with open(DIRECTORY + '\\CLIENTS\\' + 'names_and_passwords.txt', 'w', encoding='utf-8') as user: user.write(nameAndPassword)
                connection.send('ok'.encode())
                HISTORY.append((TODAYS_DATE, 'creating account', 'registration completed', client))
        # Logging in
        elif registerOrLogin == '1':
            nameAndPassword = connection.recv(BUFFER).decode()
            if nameAndPassword in NAMES_AND_PASSWORDS:
                nameAndPassword = eval(nameAndPassword)
                connection.send('ok'.encode())
                HISTORY.append((TODAYS_DATE, 'logging in', 'successful', f'{nameAndPassword[0]}:{client}'))
                print(f'login: {nameAndPassword[0]} {client}')
                break
            else:
                connection.send('wrong'.encode())
                HISTORY.append((TODAYS_DATE, 'logging in', 'access denied', client, nameAndPassword))
        else:
            ...

# ========================================================================================================

creating_folder('\\HISTORY\\')
creating_folder('\\CLIENTS\\')
creating_folder('names_and_passwords.txt')
print('Reading "names_and_passwords.txt"')
with open(DIRECTORY + '\\CLIENTS\\' + 'names_and_passwords.txt', 'r', encoding='utf-8') as lines: NAMES_AND_PASSWORDS = lines.readlines()

try:
    socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketServer.bind(('0.0.0.0', 50000))
    socketServer.listen(5)
except: 
    print(f'\nERRO...:{sys.exc_info()}')
    HISTORY.append((TODAYS_DATE, 'server activation', f'ERRO...:{sys.exc_info()}'))
    sys.exit()
else:
    print('\nThe server is active\n')
    HISTORY.append((TODAYS_DATE, 'server activation', 'sucessful activation'))

try:
    while True:
        connection, client = socketServer.accept()
        tREGISTER_LOGIN = threading.Thread(target=register_login, args=(connection, client,))
        tREGISTER_LOGIN.start()
        HISTORY.append((TODAYS_DATE, 'connection', client))
except:
    print(f'\nERRO...:{sys.exc_info()}')
