import socket, sys

host = input('\nInforme o host: ')

try:
    ip = socket.gethostbyname(host)
except:
    print(f'ERRO...:{sys.exc_info()[0]}')
else:
    print(ip)