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

# Descobrindo qual o PROTOCOLO que sera usado.
while True:
    print('\n1 - IPV4')
    print('2 - IPV6')
    mensagem  = 'Qual o protocolo: '
    protocolo = verificador_de_valor(protocolo)
    if protocolo == 1 or protocolo == 2:
        break
    else:
        print('ESCOLHA APENAS 1 OU 2.')

# Recebendo a QUANTIDADE DE DADOS que serão transportados.
mensagem  = '\nQuantidade de dados: '
quantidade_dados_ini = verificador_de_valor(quantidade_dados_ini)

# Recebendo o tamanho do CABEÇALHO. O IPV6 tem um valor fixo de 40.
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

# Recebendo quantos ENLACES/NÓS existem no caminho.
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

# Dependendo do protocolo escolhido, o código seguirá um de dois caminhos.
# O protocolo IPV6 fragmenta os dados de acordo com a menor MTU entre a origem e o destino.
# O protocolo IPV4 faz a fragmentação de no caminho, de acordo com a MTU que aparece.

# Se o valor da variável for 2, o protocolo escolhido foi o IPV6.
if protocolo == 2:
    more_fragment = 1
    menor_mtu     = min(mtus)
    area_de_dados = ((menor_mtu - cabecalho) // 8) * 8
    dados_transportados = 0
    while quantidade_dados_ini > 0:
        # Se a quantidade de dados for MENOR OU IGUAL a área de dados do datagrama.
        if quantidade_dados_ini <= area_de_dados:
            more_fragment         = 0
            dados_do_pacote       = quantidade_dados_ini
            quantidade_dados_ini -= quantidade_dados_ini
            total_len             = dados_do_pacote + cabecalho
            offset_do_datagrama   = dados_transportados // 8
            print_dos_dados(more_fragment, cabecalho, dados_do_pacote, total_len, offset_do_datagrama)
        # Se a quantidade de dados for MAIOR que a área de dados do datagrama.
        else:
            more_fragment         = 1
            quantidade_dados_ini -= area_de_dados
            dados_do_pacote       = area_de_dados
            total_len             = dados_do_pacote + cabecalho
            offset_do_datagrama   = dados_transportados // 8
            dados_transportados  += dados_do_pacote
            print_dos_dados(more_fragment, cabecalho, dados_do_pacote, total_len, offset_do_datagrama)

# Se o valor da variável for 1, o protocolo escolhido foi o IPV4.
else:
    enlace   = 1
    dados    = [quantidade_dados_ini + cabecalho]  # Lista usada para armazenar dados para a fragmentação. Ela tem seus valores subistituidos a cada laço.
    dados_para_subir = list()  # Lista que substituirá a lista "dados".
    # Uma MTU é escolhida para que os cálculos sejam feitos.
    for mtu in mtus:
        print(f'{enlace}° enlace (MTU de {mtu})\n')
        more_fragment = contador_de_loop = 1
        area_de_dados = ((mtu - cabecalho) // 8) * 8
        ultimo_confirmado   = False
        dados_transportados = 0  # Valor usado para calcular o offset.
        # De acordo com a MTU escolhida, todos os datagramas seram comparados para saber se tem o tamanho adequado.
        for indice in dados:
            if contador_de_loop == len(dados):
                ultimo_confirmado = True
            # Entraram nessa parte os datagramas que são MENORES OU IGUAIS a MTU.
            if indice <= mtu:
                if ultimo_confirmado == True:
                    more_fragment = 0
                dados_do_pacote      = indice - cabecalho
                total_len            = indice
                offset_do_datagrama  = dados_transportados // 8
                dados_transportados += dados_do_pacote
                dados_para_subir.append(indice)
                print_dos_dados(more_fragment, cabecalho, dados_do_pacote, total_len, offset_do_datagrama)
            # A entraram os datagramas que são MAIORES que a MTU para seren refragmentados.
            else:
                indice -= cabecalho
                while indice > 0:
                    offset_do_datagrama = dados_transportados // 8
                    if indice <= area_de_dados:
                        dados_do_pacote = indice
                        total_len       = dados_do_pacote + cabecalho
                        indice         -= indice
                        if ultimo_confirmado == True:
                            more_fragment = 0
                    else:
                        indice         -= area_de_dados
                        dados_do_pacote = area_de_dados
                        total_len       = area_de_dados + cabecalho
                    dados_transportados += dados_do_pacote
                    dados_para_subir.append(total_len)
                    print_dos_dados(more_fragment, cabecalho, dados_do_pacote, total_len, offset_do_datagrama)
            contador_de_loop += 1
        enlace   += 1
        dados = list()  # Esvaziando lista para receber os valores novos. 
        dados = dados_para_subir  # Recebendo os valores novos da lista secondaria.
        dados_para_subir = list()  # Esvaziando a lista.
