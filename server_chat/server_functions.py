import sys, os, datetime, threading

NAMES_AND_PASSWORDS = list()
ONLINE_CLIENTS      = list()
HISTORY             = list()
BUFFER              = 1024
DIRECTORY           = os.path.dirname(os.path.abspath(__file__))

def deactivating():
    writingHistory()
    sys.exit()

def creatingFolders(folderName):
    try:
        print(f'Creating "{folderName}"')
        os.mkdir(DIRECTORY + folderName)
    except FileExistsError: 
        print(f'  --> "{folderName}" already exists')
        HISTORY.append((str(datetime.datetime.now()), f'creating {folderName}', 'FileExistsError'))
    except: 
        print(f'\nERROR...:{sys.exc_info()[0]}')
        HISTORY.append((str(datetime.datetime.now()), f'creating {folderName}', {sys.exc_info()[0]}))
    else:
        print(f'  --> "{folderName}" was created')
        HISTORY.append((str(datetime.datetime.now()), f'creating {folderName}', 'Successfully created'))

def creatingFiles(fileName):
    try:
        print(f'Creating "{fileName}"')
        if   fileName == 'names_and_passwords.txt': path = DIRECTORY + '\\CLIENTS\\' + fileName
        elif fileName == str(datetime.date.today()): path = DIRECTORY + '\\HISTORY\\' + fileName + '.txt'
        if os.path.exists(path):
            raise FileExistsError
        else:
            with open(path, 'w'): pass
    except FileExistsError: 
        print(f'  --> "{fileName}" already exists')
        HISTORY.append((str(datetime.datetime.now()), f'creating {fileName}', 'FileExistsError'))
        if fileName == 'names_and_passwords.txt': readingTheFileOfNamesAndPasswords()
    except: 
        print(f'\nERROR...:{sys.exc_info()[0]}')
        HISTORY.append((str(datetime.datetime.now()), f'creating {fileName}', {sys.exc_info()[0]}))
    else:
        print(f'  --> "{fileName}" was created')
        HISTORY.append((str(datetime.datetime.now()), f'creating {fileName}', 'Successfully created'))

def readingTheFileOfNamesAndPasswords():
    global NAMES_AND_PASSWORDS
    print('Reading "names_and_passwords.txt"')
    with open(DIRECTORY + '\\CLIENTS\\' + 'names_and_passwords.txt', 'r', encoding='utf-8') as lines: NAMES_AND_PASSWORDS = lines.read().split('\n')
    print('  --> Extracted data')

def writingHistory():
    global HISTORY
    with open(DIRECTORY + '\\HISTORY\\' + f'{str(datetime.date.today())}.txt', 'a', encoding='utf-8') as pen:
        for line in HISTORY: pen.write(str(line) + '\n')
        HISTORY = list()

def loggingInOrCreatingAnAccount(connection, client):
    while True:
        try:
            registerOrLogin = connection.recv(BUFFER).decode()
            if registerOrLogin == '0':
                creatingAnAccount(connection, client)
            elif registerOrLogin == '1':
                confirmation = loggingIn(connection, client)
                if confirmation == 'finished': break
        except:
            print(f'\nError {sys.exc_info()} while logging in or creating an account.')
            HISTORY.append((str(datetime.datetime.now()), client, f'\nERROR...:{sys.exc_info()[0]}'))

def creatingAnAccount(connection, client):
    nameAndPassword = connection.recv(BUFFER).decode()
    found = False
    if NAMES_AND_PASSWORDS != ['']:
        for name in NAMES_AND_PASSWORDS:
            if name != '' and eval(name)[0] == eval(nameAndPassword)[0]: 
                found = True
                break
    if found == True:
        connection.send('wrong'.encode())
        HISTORY.append((str(datetime.datetime.now()), 'creating account', 'name unavailable', client))
    else: 
        NAMES_AND_PASSWORDS.append(nameAndPassword)
        with open(DIRECTORY + '\\CLIENTS\\' + 'names_and_passwords.txt', 'a', encoding='utf-8') as user: user.write(nameAndPassword + '\n')
        connection.send('ok'.encode())
        HISTORY.append((str(datetime.datetime.now()), 'creating account', 'registration completed', client))

def loggingIn(connection, client):
    nameAndPassword = connection.recv(BUFFER).decode()
    if nameAndPassword in NAMES_AND_PASSWORDS:
        ONLINE_CLIENTS.append((eval(nameAndPassword)[0], client, connection))
        connection.send('ok'.encode())
        HISTORY.append((str(datetime.datetime.now()), 'logging in', 'successful', f'{eval(nameAndPassword)[0]}:{client}'))
        print(f'login: {eval(nameAndPassword)[0]} {client}')
        tCHATS = threading.Thread(target=forwardingMessages, args=(connection, client,))
        tCHATS.start()
        writingHistory()
        return 'finished'
    else:
        connection.send('wrong'.encode())
        HISTORY.append((str(datetime.datetime.now()), 'logging in', 'access denied', client, nameAndPassword))

def forwardingMessages(connection, client):
    while True:
        try:
            message = connection.recv(BUFFER).decode()
            for nameClientConnection in ONLINE_CLIENTS:
                if not nameClientConnection[1] == client:
                    nameClientConnection[2].send(message.encode())
        except KeyboardInterrupt as errorType:
            print(f'\nERROR {errorType}. Abrupt disconnection.')
            HISTORY.append((str(datetime.datetime.now()), errorType, client, 'abrupt disconnction'))
        except:
            print(f'\nERROR...:{sys.exc_info()}')
            HISTORY.append((str(datetime.datetime.now()), sys.exc_info(), client))
