# OBS: AINDA ESTOU DESENVOLVENDO A REFRAGMENTAÇÃO. Por enquanto ele só faz os cálculos para uma fragmentação.

# Código feito para calcular a fragmentação de datagramas.
#-------------------------------------------------------------------------


quantidade_dados_ini = int(input('\nQuantidade de dados em bytes...: '))
tamanho_cabecalho    = int(input('Tamanho do cabeçalho em bytes..: '))
quantidade_enlaces   = int(input('Quantidade de enlaces..........: '))
print('\n')

mtus = list()
for turn in range(quantidade_enlaces):
    capacidade_mtu = int(input(f'Informe a MTU do {turn + 1}° enlace: '))
    mtus.append(capacidade_mtu)
print('\n', 100 * '-')

for mtu in mtus:
    contador = 1
    offset =  mtu  = (mtu - tamanho_cabecalho) // 8   # Subtraindo o cabeçalho e descobrindo o offset.
    area_de_dados  =  mtu * 8   # Obtendo a quantidade de dados por pacote/datagrama.

    dados = list()   # Lista usada para armazenar dados para a fragmentação.
    if contador == 1:
        dados.append(quantidade_dados_ini)
    
    for index in dados:
        quantidade_fragmentos = index // area_de_dados   # Quantidade de fragmentos. Resultado decimal, adiciona mais um fragmento.
        if index % area_de_dados > 0 or quantidade_fragmentos == 0:
            quantidade_fragmentos += 1
            
        print('\n')
        quantidade_dados = index
        fragmento = 1
        offset_do_datagrama = 0
        dados_para_subir = list()
        for turn in range(quantidade_fragmentos):   # Descobrindo se haverá mais fragmentos e a quantidade de dados do pacote
            if quantidade_dados <= area_de_dados:
                mf = 0
                dados_do_pacote = quantidade_dados
            else:
                mf = 1
                quantidade_dados -= area_de_dados
                dados_do_pacote = area_de_dados

            dados_para_subir.append(dados_do_pacote + tamanho_cabecalho)

            print(f'\nFRAGMENTO {fragmento}:\n')
            print(f'MORE FRAGMENT.........: {mf}')
            print(f'HLEN (BYTES)..........: {tamanho_cabecalho}')
            print(f'DATA (BYTES)..........: {dados_do_pacote}')
            print(f'TOTAL LENGTH (BYTES)..: {dados_do_pacote + tamanho_cabecalho}')
            print(f'FRAGMENT OFFSET.......: {offset_do_datagrama}')
            print(100 * '-')

            fragmento += 1
            offset_do_datagrama += offset
    contador += 1
    dados = list()
    dados.append(dados_para_subir)
    dados_para_subir = list()
