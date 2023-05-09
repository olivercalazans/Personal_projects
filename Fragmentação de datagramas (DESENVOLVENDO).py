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
print('\n')
print(100 * '-')

enlace   = 1
dados    = [quantidade_dados_ini + tamanho_cabecalho]  # Lista usada para armazenar dados para a fragmentação. Ela tem seus valores subistituidos a cada laço.
dados_para_subir = list()  # Lista que substituirá a lista "dados".
for mtu in mtus:
    print(f'{enlace}° enlace (MTU de {mtu})\n')
    offset = (mtu - tamanho_cabecalho) // 8   # Subtraindo o cabeçalho e descobrindo o offset.
    area_de_dados = offset * 8   # Obtendo a quantidade de dados por pacote/datagrama.

    mf = 1
    offset_do_datagrama = 0
    ultimo_fragmento = dados[-1]
    ultimo_confirmado = False
    for index in dados:
        if index == ultimo_fragmento:
            ultimo_confirmado = True
        if index <= mtu:
            dados_do_pacote = index - tamanho_cabecalho
            if ultimo_confirmado == True:
                mf = 0
            print(f'MORE FRAGMENT.........: {mf}')
            print(f'HLEN (BYTES)..........: {tamanho_cabecalho}')
            print(f'DATA (BYTES)..........: {dados_do_pacote}')
            print(f'TOTAL LENGTH (BYTES)..: {index}')
            print(f'FRAGMENT OFFSET.......: {offset_do_datagrama}')
            print(100 * '-')
            dados_para_subir.append(index)
        else:
            index -= tamanho_cabecalho
            while index > 0:
                if index <= area_de_dados:
                    dados_do_pacote = index
                    total_len = dados_do_pacote + tamanho_cabecalho
                    index -= index
                    if ultimo_confirmado == True:
                        mf = 0
                else:
                    index -= area_de_dados
                    dados_do_pacote = area_de_dados
                    total_len = area_de_dados + tamanho_cabecalho
            
                dados_para_subir.append(total_len)

                print(f'MORE FRAGMENT.........: {mf}')
                print(f'HLEN (BYTES)..........: {tamanho_cabecalho}')
                print(f'DATA (BYTES)..........: {dados_do_pacote}')
                print(f'TOTAL LENGTH (BYTES)..: {total_len}')
                print(f'FRAGMENT OFFSET.......: {offset_do_datagrama}')
                print(100 * '-')

                offset_do_datagrama += offset
    
    enlace   += 1
    dados = list()
    dados = dados_para_subir
    dados_para_subir = list()


    # RESOLVER O PROBLEMA DO OFFSET
