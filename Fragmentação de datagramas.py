# Código feito para calcular a fragmentação de datagramas.
#-------------------------------------------------------------------------

import sys

while True:
    try:
        quantidade_dados_ini = int(input('\nQuantidade de dados em bytes...: '))
    except ValueError:
        print('DIGITE APENAS NÚMEROS.')
    except:
        print(f'ERRO...:{sys.exc_info()[0]}')
    else:
        break

while True:
    try:
        tamanho_cabecalho = int(input('\nTamanho do cabeçalho em bytes..: '))
    except ValueError:
        print('DIGITE APENAS NÚMEROS.')
    except:
        print(f'ERRO...:{sys.exc_info()[0]}')
    else:
        break

while True:
    try:
        quantidade_enlaces = int(input('\nQuantidade de enlaces..........: '))
    except ValueError:
        print('DIGITE APENAS NÚMEROS.')
    except:
        print(f'ERRO...:{sys.exc_info()[0]}')
    else:
        break

print('\n')

mtus = list()
for turn in range(quantidade_enlaces):
    while True:
        try: 
            capacidade_mtu = int(input(f'Informe a MTU do {turn + 1}° enlace: '))
        except ValueError:
            print('DIGITE APENAS NÚMEROS.')
        except:
            print(f'ERRO...:{sys.exc_info()[0]}')
        else:
            mtus.append(capacidade_mtu)
            break

print('\n')
print(100 * '-')

enlace   = 1
dados    = [quantidade_dados_ini + tamanho_cabecalho]  # Lista usada para armazenar dados para a fragmentação. Ela tem seus valores subistituidos a cada laço.
dados_para_subir = list()  # Lista que substituirá a lista "dados".
for mtu in mtus:
    print(f'{enlace}° enlace (MTU de {mtu})\n')
    area_de_dados = ((mtu - tamanho_cabecalho) // 8) * 8   # Obtendo a quantidade de dados por pacote/datagrama.

    mf = 1
    contador_de_loop  = 1 
    ultimo_loop       = len(dados)
    dados_do_offset   = 0
    ultimo_confirmado = False
    for index in dados:
        if contador_de_loop == ultimo_loop:
            ultimo_confirmado = True
        if index <= mtu:
            dados_do_pacote = index - tamanho_cabecalho
            if ultimo_confirmado == True:
                mf = 0
            offset_do_datagrama = dados_do_offset // 8
            print(f'MORE FRAGMENT.........: {mf}')
            print(f'HLEN (BYTES)..........: {tamanho_cabecalho}')
            print(f'DATA (BYTES)..........: {dados_do_pacote}')
            print(f'TOTAL LENGTH (BYTES)..: {index}')
            print(f'FRAGMENT OFFSET.......: {offset_do_datagrama}')
            print(100 * '-')
            dados_para_subir.append(index)
            dados_do_offset += dados_do_pacote
        else:
            index -= tamanho_cabecalho
            while index > 0:
                offset_do_datagrama = dados_do_offset // 8
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

                dados_do_offset += dados_do_pacote
        contador_de_loop += 1
    
    enlace   += 1
    dados = list()
    dados = dados_para_subir
    dados_para_subir = list()
