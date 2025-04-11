import pandas as pd
import unicodedata
import re
from collections import defaultdict

def normalize_name(name):
    name = name.upper().strip()
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')  # remove acentos
    name = re.sub(r"[^A-Z0-9 ]", "", name)  # remove pontuação
    words = sorted(name.split())  # ordena as palavras
    return " ".join(words)

def gerar_de_para(path_entrada_txt, path_saida_csv):
    with open(path_entrada_txt, 'r', encoding='utf-8') as f:
        nomes = list(set([line.strip() for line in f.readlines() if line.strip()]))

    agrupado = defaultdict(list)
    for nome in nomes:
        chave = normalize_name(nome)
        agrupado[chave].append(nome)

    de_para = []
    for chave, lista_nomes in agrupado.items():
        nome_padrao = max(lista_nomes, key=lambda x: len(x.split()))
        for nome in lista_nomes:
            de_para.append({
                "Nome Original": nome,
                "Nome Padronizado": nome_padrao
            })

    df = pd.DataFrame(de_para).drop_duplicates().sort_values("Nome Padronizado")
    df.to_csv(path_saida_csv, sep=";", index=False, encoding="utf-8-sig")
    print(f"Tabela De-Para exportada para: {path_saida_csv}")

if __name__ == "__main__":
    gerar_de_para("lista.txt", "de_para.csv")

# Exemplo de uso:
# gerar_de_para("fornecedores.txt", "de_para_fornecedores.csv")
