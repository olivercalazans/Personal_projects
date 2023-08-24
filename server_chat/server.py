import datetime, os, sys, socket, threading

# ============================================ CONSTANTS =================================================
NAMES_AND_PASSWORDS = list()
ONLINE_CLIENTS      = list()
HISTORY             = list()
BUFFER              = 1024
TODAYS_DATE         = str(datetime.date.today())
DIRECTORY           = os.path.dirname(os.path.abspath(__file__))
# ============================================ FUNCTIONS =================================================
def deactivating():
    writingHistory()
    sys.exit()

def creatingFoldersAndFile(folderName):
    try:
        print(f'Creating "{folderName}"')
        if folderName == 'names_and_passwords.txt':
            if os.path.exists(DIRECTORY + '\\CLIENTS\\' + folderName): raise FileExistsError
            else:
                with open(DIRECTORY + '\\CLIENTS\\' + folderName, 'w'): pass
        else: os.mkdir(DIRECTORY + folderName)
    except FileExistsError: 
        print(f'  --> "{folderName}" already exists')
        HISTORY.append((TODAYS_DATE, f'creating {folderName}', 'FileExistsError'))
        if folderName == 'names_and_passwords.txt': readingTheFileOfNamesAndPasswords()
    except: 
        print(f'\nERROR...:{sys.exc_info()[0]}')
        HISTORY.append((TODAYS_DATE, f'creating {folderName}', {sys.exc_info()[0]}))
    else:
        print(f'  --> "{folderName}" was created')
        HISTORY.append((TODAYS_DATE, f'creating {folderName}', 'Successfully created'))

def readingTheFileOfNamesAndPasswords():
    global NAMES_AND_PASSWORDS
    print('Reading "names_and_passwords.txt"')
    with open(DIRECTORY + '\\CLIENTS\\' + 'names_and_passwords.txt', 'r', encoding='utf-8') as lines: NAMES_AND_PASSWORDS = lines.read().split('\n')
    print('  --> Extracted data')

def writingHistory():
    with open(DIRECTORY + '\\CLIENT\\' + 'names_and_passwords.txt', 'w', encoding='utf-8') as pen:
        for line in HISTORY: pen.write(line)
        HISTORY = list()

def loggingInOrCreatingAnAccount(connection, client):
    try:
        while True:
            registerOrLogin = connection.recv(BUFFER).decode()
            # Registration
            if registerOrLogin == '0':
                nameAndPassword = connection.recv(BUFFER).decode()
                found = False
                if NAMES_AND_PASSWORDS != ['']:
                    for name in NAMES_AND_PASSWORDS:
                        if name != '' and eval(name)[0] == eval(nameAndPassword)[0]: 
                            found = True
                            break
                if found == True:
                    connection.send('wrong'.encode())
                    HISTORY.append((TODAYS_DATE, 'creating account', 'name unavailable', client))
                else: 
                    NAMES_AND_PASSWORDS.append(nameAndPassword)
                    with open(DIRECTORY + '\\CLIENTS\\' + 'names_and_passwords.txt', 'a', encoding='utf-8') as user: user.write(nameAndPassword + '\n')
                    connection.send('ok'.encode())
                    HISTORY.append((TODAYS_DATE, 'creating account', 'registration completed', client))
            # Logging in
            elif registerOrLogin == '1':
                nameAndPassword = connection.recv(BUFFER).decode()
                if nameAndPassword in NAMES_AND_PASSWORDS:
                    connection.send('ok'.encode())
                    HISTORY.append((TODAYS_DATE, 'logging in', 'successful', f'{eval(nameAndPassword)[0]}:{client}'))
                    print(f'login: {eval(nameAndPassword)[0]} {client}')
                    tCHATS = threading.Thread(target=chats, args=(connection, client,))
                    tCHATS.start()
                    break
                else:
                    connection.send('wrong'.encode())
                    HISTORY.append((TODAYS_DATE, 'logging in', 'access denied', client, nameAndPassword))
    except:
        print(f'\nERROR...:{sys.exc_info()[0]}')
        HISTORY.append((TODAYS_DATE, client, f'\nERROR...:{sys.exc_info()[0]}'))

def chats(connetion, client):
    ...


# ========================================================================================================

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
