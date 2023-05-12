# Código feito para calcular a fragmentação de datagramas.
#-------------------------------------------------------------------------

import sys

# Todos os dados começam vazios.
quantidade_dados_ini = tamanho_cabecalho = quantidade_enlaces = protocolo = mensagem = capacidade_mtu = ''

# Função criada para evitar a repetição dos mesmos laços na hora de receber os valores.
# O objetivo dessa função é evitar valores que não correspondem com os cáculos.
def verificador_de_valor(valor):
    while True:
        try:
            valor = int(input(f'{mensagem}'))
        except ValueError:
            print('DIGITE APENAS NÚMEROS.\n')
        except:
            print(f'ERRO...:{sys.exc_info()[0]}')
        else:
            return valor
            break

# Descobrindo qual o protocolo que sera usado.
while True:
    print('\n1 - IPV4')
    print('2 - IPV6')
    mensagem  = 'Qual o protocolo: '
    protocolo = verificador_de_valor(protocolo)
    if protocolo == 1 or protocolo == 2:
        break
    else:
        print('ESCOLHA APENAS 1 OU 2.')

# Recebendo a quantidade de dados que serão transportados.
mensagem  = '\nQuantidade de dados: '
quantidade_dados_ini = verificador_de_valor(quantidade_dados_ini)

# Recebendo o tamanho do cabeçalho. O IPV6 tem um valor fixo de 40.
if protocolo == 2:
    tamanho_cabecalho = 40
else:
    while True:
        mensagem  = '\nTamanho do cabeçalho: '
        tamanho_cabecalho = verificador_de_valor(tamanho_cabecalho)
        if tamanho_cabecalho >= 20 and tamanho_cabecalho <= 60:
            break
        else:
            print('O cabeçalho do IPV4 fica entre 20 e 60.')

# Recebendo quantos enlaces/nós existem no caminho
mensagem  = '\nQuantidade de enlaces/nós: '
quantidade_enlaces = verificador_de_valor(quantidade_enlaces)

print('\n')

mtus = list()
for turn in range(quantidade_enlaces):
    mensagem  = f'Informe o tamamanho da {turn + 1} MTU: '
    capacidade_mtu = verificador_de_valor(capacidade_mtu)
    mtus.append(capacidade_mtu)

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
