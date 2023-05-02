quantidade_dados_ini = int(input('Quantidade de dados em bytes: '))
tamanho_cabecalho    = int(input('Tamanho do cabeçalho em bytes: '))
quantidade_enlaces   = int(input('Quantidade de enlaces: '))
mtus = []
for turn in range(quantidade_enlaces):
    capacidade_mtu = int(input('Informe a MTU dos enlaces: '))
    mtus.append(capacidade_mtu)

for mtu in mtus:
    mtu = mtu - 20 # Subitraindo o cabeçalho.
    mtu = mtu // 8 # Descobrindo o offset
    offset = mtu
    mtu = mtu * 8 # Descobrindo a quantidade de dados por pacote/datagrama
    
    # Quantidade de fragmentos. Resultado fragmentado, adiciona mais um fragmento.
    quantidade_fragmentos = quantidade_dados_ini // mtu 
    if quantidade_dados_ini % mtu > 0:
        quantidade_fragmentos += 1
    
    quantidade_dados = quantidade_dados_ini
    for turn in range(quantidade_fragmentos): 
