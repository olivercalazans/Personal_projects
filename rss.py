
from googlesearch import search

PALAVRA_CHAVE = input('>')

results = search(PALAVRA_CHAVE, num=10, stop=10, pause=2)

print(f'As 10 URLs das notícias sobre "{PALAVRA_CHAVE}":')

for i, url in enumerate(results):
    print(f'{i}. {url}')
