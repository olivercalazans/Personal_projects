# OBS: AINDA ESTOU DESENVOLVENDO A REFRAGMENTAÇÃO. Por enquanto ele só faz os cálculos para uma fragmentação.

# Código feito para calcular a fragmentação de datagramas.
#-------------------------------------------------------------------------

quantidade_dados_ini = int(input('\nQuantidade de dados em bytes...: '))
tamanho_cabecalho    = int(input('Tamanho do cabeçalho em bytes..: '))
quantidade_enlaces   = int(input('Quantidade de enlaces..........: '))
mtus = []
for turn in range(quantidade_enlaces):
    capacidade_mtu = int(input('Informe a MTU dos enlaces: '))
    mtus.append(capacidade_mtu)
print('\n', 100 * '-')

lista_de_fragmentos = [] # Lista feita para armazenar informações e para o funcionamento do código.
                         # Ordem da lista: FRAGMENTO, MORE FRAGMENT, HLEN, DATA, TOTAL LENGTH, OFFSET.

for mtu in mtus:
    mtu = mtu - 20 # Subtraindo o cabeçalho.
    mtu = mtu // 8 # Obtendo o offset.
    offset = mtu
    mtu = mtu * 8 # Obtendo a quantidade de dados por pacote/datagrama.
    
    # Quantidade de fragmentos. Resultado fragmentado, adiciona mais um fragmento.
    quantidade_fragmentos = quantidade_dados_ini // mtu 
    if quantidade_dados_ini % mtu > 0:
        quantidade_fragmentos += 1
    
    fragmento_salvar = []

    print('\n')
    quantidade_dados = quantidade_dados_ini
    fragmento = 1
    offset_do_datagrama = 0
    for turn in range(quantidade_fragmentos):
        # Descobrindo se haverá mais fragmentos e a quantidade de dados do pacote
        if quantidade_dados <= mtu:
            mf = 0
            dados_do_pacote = quantidade_dados
        else:
            mf = 1
            quantidade_dados -= mtu
            dados_do_pacote = mtu
        
        fragmento_interno = []
        fragmento_interno.append(fragmento)
        fragmento_interno.append(mf)
        fragmento_interno.append(tamanho_cabecalho)
        fragmento_interno.append(dados_do_pacote)
        fragmento_interno.append(dados_do_pacote + tamanho_cabecalho)
        fragmento_interno.append(offset_do_datagrama)

        fragmento_salvar.append(fragmento_interno)

        print(f'\nFRAGMENTO {fragmento}:\n')
        print(f'MORE FRAGMENT.........: {mf}')
        print(f'HLEN (BYTES)..........: {tamanho_cabecalho}')
        print(f'DATA (BYTES)..........: {dados_do_pacote}')
        print(f'TOTAL LENGTH (BYTES)..: {dados_do_pacote + tamanho_cabecalho}')
        print(f'FRAGMENT OFFSET.......: {offset_do_datagrama}')
        print(100 * '-')
        fragmento += 1
        offset_do_datagrama += offset

    lista_de_fragmentos.append(fragmento_salvar)
