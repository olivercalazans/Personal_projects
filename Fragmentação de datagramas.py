# Código feito para calcular a fragmentação de datagramas.
#-------------------------------------------------------------------------

import sys

#===================================== BLOCO DE ENTRADA DE DADOS ===================================================
# Todos os dados começam vazios.
quantidade_dados_ini = cabecalho = quantidade_enlaces = protocolo = mensagem = capacidade_mtu = ''

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
    cabecalho = 40
else:
    while True:
        mensagem  = '\nTamanho do cabeçalho: '
        cabecalho = verificador_de_valor(cabecalho)
        if cabecalho >= 20 and cabecalho <= 60:
            break
        else:
            print('O cabeçalho do IPV4 fica entre 20 e 60.')

# Recebendo quantos enlaces/nós existem no caminho.
mensagem  = '\nQuantidade de enlaces/nós: '
quantidade_enlaces = verificador_de_valor(quantidade_enlaces)

print('\n')

# Recebendo os valores das MTUs.
mtus = list()
for turn in range(quantidade_enlaces):
    mensagem  = f'Informe o tamamanho da {turn + 1}° MTU: '
    capacidade_mtu = verificador_de_valor(capacidade_mtu)
    mtus.append(capacidade_mtu)

print('\n')
print(100 * '-')


#========================================= BLOCO DE PROCESSAMENTO ========================================
# Função usada para evitar a repetição dos mesmos prints.
def print_dos_dados(more_fragment, tamanho_cabecalho, dados_do_pacote, total_len, offset_do_datagrama):
    print(f'MORE FRAGMENT.........: {more_fragment}')
    print(f'HLEN (BYTES)..........: {tamanho_cabecalho}')
    print(f'DATA (BYTES)..........: {dados_do_pacote}')
    print(f'TOTAL LENGTH (BYTES)..: {total_len}')
    print(f'FRAGMENT OFFSET.......: {offset_do_datagrama}')
    print(100 * '-')


if protocolo == 2:
    more_fragment = 1
    menor_mtu     = min(mtus)
    area_de_dados = ((menor_mtu - cabecalho) // 8) * 8
    dados_transportados = 0
    while quantidade_dados_ini > 0:
        if quantidade_dados_ini <= area_de_dados:
            more_fragment   = 0
            dados_do_pacote = quantidade_dados_ini
            quantidade_dados_ini -= quantidade_dados_ini
            total_len = dados_do_pacote + cabecalho
            offset_do_datagrama = dados_transportados // 8
            print_dos_dados(more_fragment, cabecalho, dados_do_pacote, total_len, offset_do_datagrama)
        else:
            more_fragment = 1
            quantidade_dados_ini -= area_de_dados
            dados_do_pacote = area_de_dados
            total_len = dados_do_pacote + cabecalho
            offset_do_datagrama = dados_transportados // 8
            print_dos_dados(more_fragment, cabecalho, dados_do_pacote, total_len, offset_do_datagrama)
            dados_transportados += dados_do_pacote
else:
    enlace   = 1
    dados    = [quantidade_dados_ini + cabecalho]  # Lista usada para armazenar dados para a fragmentação. Ela tem seus valores subistituidos a cada laço.
    dados_para_subir = list()  # Lista que substituirá a lista "dados".
    for mtu in mtus:
        print(f'{enlace}° enlace (MTU de {mtu})\n')
        area_de_dados = ((mtu - cabecalho) // 8) * 8   # Obtendo a quantidade de dados por pacote/datagrama.

        more_fragment = 1
        contador_de_loop  = 1 
        ultimo_loop       = len(dados)
        dados_transportados   = 0
        ultimo_confirmado = False
        for index in dados:
            if contador_de_loop == ultimo_loop:
                ultimo_confirmado = True
            if index <= mtu:
                dados_do_pacote = index - cabecalho
                total_len = index
                if ultimo_confirmado == True:
                    more_fragment = 0
                offset_do_datagrama = dados_transportados // 8
                print(f'MORE FRAGMENT.........: {more_fragment}')
                print(f'HLEN (BYTES)..........: {cabecalho}')
                print(f'DATA (BYTES)..........: {dados_do_pacote}')
                print(f'TOTAL LENGTH (BYTES)..: {total_len}')
                print(f'FRAGMENT OFFSET.......: {offset_do_datagrama}')
                print(100 * '-')
                dados_para_subir.append(index)
                dados_transportados += dados_do_pacote
            else:
                index -= cabecalho
                while index > 0:
                    offset_do_datagrama = dados_transportados // 8
                    if index <= area_de_dados:
                        dados_do_pacote = index
                        total_len = dados_do_pacote + cabecalho
                        index -= index
                        if ultimo_confirmado == True:
                            more_fragment = 0
                    else:
                        index -= area_de_dados
                        dados_do_pacote = area_de_dados
                        total_len = area_de_dados + cabecalho
                
                    dados_para_subir.append(total_len)

                    print(f'MORE FRAGMENT.........: {more_fragment}')
                    print(f'HLEN (BYTES)..........: {cabecalho}')
                    print(f'DATA (BYTES)..........: {dados_do_pacote}')
                    print(f'TOTAL LENGTH (BYTES)..: {total_len}')
                    print(f'FRAGMENT OFFSET.......: {offset_do_datagrama}')
                    print(100 * '-')

                    dados_transportados += dados_do_pacote
            contador_de_loop += 1
        
        enlace   += 1
        dados = list()
        dados = dados_para_subir
        dados_para_subir = list()
