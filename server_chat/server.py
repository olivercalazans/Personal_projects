import datetime, os, sys, socket


# ============================================ CONSTANTS =================================================

ALL_CLIENTS = list()
HISTORY     = list()
BUFFER      = 2048
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

# ========================================================================================================

print('Creating folder for history')
creating_folder('\\HISTORY\\')

print('Creating folder for clients')
creating_folder('\\CLIENTS\\')

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind('0.0.0.0', 50000)
    sock.listen(5)
except: 
    print(f'\nERRO...:{sys.exc_info()}')
    sys.exit()
else: print('The server is active\n')

try:
    while True:
        connection, client = sock.accept()

except:
    print(f'\nERRO...:{sys.exc_info()}')
    sys.exit()

