# Esse código recebe os nomes, dos alunos, 4 notas e tira a média das notas. Ao final é possível criar um arquivo
# com os dados gerados. Antes de escrever, os dados são mostrados para que possam ser conferidos antes de serem salvos.

import sys, os

# Função para evitar a repetição dos mesmos comandos. ------------------------------------------------------------------
# Essa função aceita apenas números dentro do limite estabelecido.

def verificador_valor():
    while True:
        try:
            valor = float(input(f'{mensagem}'))
        except ValueError:
            print('DIGITE APENAS NÚMEROS.')
        except KeyboardInterrupt:
            print('\nTODOS OS DADOS NÃO SALVOS FORAM PERDIDOS!!!')
            sys.exit()
        except:
            print(f'ERRO...:{sys.exc_info()[0]}')
        else:
            if valor < 0 or valor > limite:
                print('NOTA FORA DO LIMITE!!!')
            else:
                return valor

# Área de armazenamento -----------------------------------------------------------------------------------------------
# "data" - lista que salva os dados de entrada.
# "data_wrt" - lista usada para salvar todos os dados (incluindo a média) e escrever o arquivo.

data     = list()
data_wrt = list()

# Entrada de dados ----------------------------------------------------------------------------------------------------
# Recebendo o número da turma/serie.
limite   = 10
mensagem = 'Digite o número da turma: '
serie    = verificador_valor()

while True:   # Recebendo os nomes e as 4 notas do aluno e calculando a média.
    linha = list()
    nome  = input('\nNome do aluno(a)(p/ sair "exit"): ')
    if nome == 'exit': break
    linha.append(nome)
    for loop in range(4):
        mensagem = f'Digite a {loop + 1} nota: '
        nota     = verificador_valor()
        linha.append(nota)
    data.append(linha)

# Apresentação --------------------------------------------------------------------------------------------------------
print('-' * 100)
print(f'\n{serie:.0f}° Ano        Nota 1       |Nota 2       |Nota 3       |Nota 4       |Média')
for nome in data:
    espaco = list()
    for dado in nome:  # Laço para descobrir o espaço entre os dados. Isso mantem os dados organizados para a escrita.
        aux = 13 - len(str(dado))
        espaco.append(aux)
    media = (nome[1] + nome[2] + nome[3] + nome[4]) / 4
    nome.append(media)
    full_line = f'{nome[0]}{f"." * espaco[0]} {nome[1]}{" " * espaco[1]}|{nome[2]}{" " * espaco[2]}|{nome[3]}{" " * espaco[3]}|{nome[4]}{" " * espaco[4]}|{nome[5]:.1f}'
    data_wrt.append(full_line)
    print(full_line)
print('\n')
print('-' * 100)

# Salvando arquivo com os dados apresentados --------------------------------------------------------------------------
while True:
    permissao = input('\nDeseja salvar um arquivo? Sim(s) / Não(n): ').upper()
    if permissao == 'S' or permissao == 'N': break

if permissao == 'S':
    # Criando uma pasta "notas" para armazenar o arquivo.
    DIRETORIO  = os.path.dirname(os.path.abspath(__file__))
    DIRETORIO += '\\notas\\'

    try:
        os.mkdir(DIRETORIO)
    except FileExistsError:
        print('\nO diretóro já existe.\n')
    except:
        print(f'ERRO...:{sys.exc_info()[0]}')
    else:
        print(f'\nDiretório criado com sucesso!!!\n')
    
    # Recebendo o número do bimestre.
    limite   = 4
    mensagem = ('Insira o número do bimestre: ')
    bimestre = verificador_valor()

    # Criando o arquivo.
    try:
        with open(DIRETORIO + f'{serie:.0f}° Ano - {bimestre:.0f}° bimestre.txt','w',encoding='utf-8') as escrevendo:
            escrevendo.write(f'{serie:.0f}° Ano        Nota 1       |Nota 2       |Nota 3       |Nota 4       |Média\n')
            for dados in data_wrt:
                escrevendo.write(f'{dados}\n')
    except:
        print(f'\nERRO...:{sys.exc_info()[0]}')
        sys.exit()
    else:
        print('\nArquivo salvo com sucesso!!!')
