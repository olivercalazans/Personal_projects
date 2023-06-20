# Fiz esse código para me ajudar a calcular a média dos alunos. 

import sys

#------------------------------------------------------------------------------------
# Função para evitar a repetição dos mesmos comandos.
# Essa função aceita apenas erro.

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
            return valor
#------------------------------------------------------------------------------------

data = list() # Lista que armazena os dados (nome, 1° nota, 2° nota, 3° nota, 4° nota, média)

mensagem = 'Digite o número da turma: '
serie    = verificador_valor()

while True:
    linha = list()
    nome  = input('\nNome do aluno(a)(p/ sair "exit"): ')
    if nome == 'exit': break
    linha.append(nome)
    for loop in range(4):
        mensagem = f'Digite a {loop + 1} nota: '
        nota     = verificador_valor()
        linha.append(nota)
    data.append(linha)

print('-' * 100)
print(f'\n{serie:.0f}° Ano        Nota 1       |Nota 2       |Nota 3       |Nota 4       |Média')
for nome in data:
    espaco = list()
    for dado in nome:  # Laço para descobrir o espaço entre os dados. Isso mantem os dados organizados para a escrita.
        aux = 13 - len(str(dado))
        espaco.append(aux)

    print(f'{nome[0]}{f"." * espaco[0]} {nome[1]}{" " * espaco[1]}|{nome[2]}{" " * espaco[2]}|{nome[3]}{" " * espaco[3]}|{nome[4]}{" " * espaco[4]}|{(nome[1] + nome[2] + nome[3] + nome[4]) / 4:.1f}')
   