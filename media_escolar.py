# Esse código recebe os nomes, dos alunos, 4 notas e tira a média das notas. Ao final é possível criar um arquivo, em excel,
# com os dados gerados. Antes de escrever, os dados são mostrados para que possam ser conferidos antes de serem salvos.

import sys, os, openpyxl

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
# "data" - lista que salva os dados de entrada. Durante o laço, ela recebe a média das notas informadas.

data = list()

# Entrada de dados ----------------------------------------------------------------------------------------------------
# Recebendo o número da turma/serie.
limite   = 10
mensagem = '\nDigite o número da turma: '
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
data.sort(key=lambda sublista: sublista[0])
print('-' * 100)
print(f'\n{serie:.0f}° Ano        Nota 1       |Nota 2       |Nota 3       |Nota 4       |Média')
for nome in data:
    espaco = list()
    for dado in nome:  # Laço para descobrir o espaço entre os dados. Isso mantem os dados organizados para a escrita.
        aux = 13 - len(str(dado))
        espaco.append(aux)
    media = round(((nome[1] + nome[2] + nome[3] + nome[4]) / 4), 1)
    nome.append(media)
    print(f'{nome[0]}{f"." * espaco[0]} {nome[1]}{" " * espaco[1]}|{nome[2]}{" " * espaco[2]}|{nome[3]}{" " * espaco[3]}|{nome[4]}{" " * espaco[4]}|{nome[5]}')
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
        livro = openpyxl.Workbook()
        pagina = livro['Sheet']
        pagina.append(['Alunos','ATV 1','Seminário','Teste','Prova','Média'])
        for linha in data:
            pagina.append(linha)
        livro.save(DIRETORIO + f'{serie:.0f}° Ano, {bimestre:.0f}° Bimestre.xlsx')
    except:
        print(f'\nERRO...:{sys.exc_info()[0]}')
        sys.exit()
    else:
        print('\nArquivo salvo com sucesso!!!')
