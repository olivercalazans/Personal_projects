# Esse código descobre o endereço de IP a partir do nome de Host.

import socket, sys

host = input('\nInforme o host: ')

try:
    ip = socket.gethostbyname(host)
    print('-' * 50)
except socket.gaierror:
    print('\nErro no nome do host.')
except:
    print(f'ERRO...:{sys.exc_info()[0]}')
else:
    print(ip)
    print('-' * 50)
