import csv
from collections import defaultdict
import os
import sys

def ler_arquivo_csv(nome_arquivo):
    quantidades = defaultdict(int)
    valores = defaultdict(float)

    if not os.path.exists(nome_arquivo):
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        sys.exit(1)

    with open(nome_arquivo, mode="r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        linhas_lidas = 0

        for linha in leitor:
            linhas_lidas += 1
            produto = linha.get("produto", "").strip()
            quantidade_str = linha.get("quantidade", "").strip()
            preco_str = linha.get("preco_unitario", "").strip()

            if not produto or not quantidade_str or not preco_str:
                print(f"Aviso: Linha {linhas_lidas + 1} ignorada por dados ausentes.")
                continue

            try:
                quantidade = int(quantidade_str)
                preco = float(preco_str.replace(",", "."))
            except ValueError:
                print(f"Aviso: Linha {linhas_lidas + 1} ignorada por dados inválidos.")
                continue

            quantidades[produto] += quantidade
            valores[produto] += quantidade * preco

    if not quantidades:
        print("Nenhum dado válido foi encontrado no arquivo.")
        sys.exit(1)

    return quantidades, valores

def calcular_resumo(quantidades, valores):
    if not quantidades or not valores:
        print("Erro: Não há dados suficientes para gerar o relatório.")
        sys.exit(1)

    produto_mais_vendido = max(quantidades, key=quantidades.get)
    valor_total_geral = sum(valores.values())
    return produto_mais_vendido, valor_total_geral

def exibir_relatorio(quantidades, valores, produto_mais_vendido, valor_total_geral):
    print("\nRelatórios de Vendas\n")
    print(f"{'Produto':<12}{'Quantidade':<12}{'Valor Total'}")
    print("-" * 40)

    for produto in quantidades:
        print(f"{produto:<12}{quantidades[produto]:<12}{valores[produto]:.2f}")

    print("\n" + "-" * 40)
    print(f"Valor total de todas as vendas: R$ {valor_total_geral:.2f}")
    print(f"Produto mais vendido: {produto_mais_vendido} ({quantidades[produto_mais_vendido]} unidades)")

def main():
    nome_arquivo = "vendas.csv"
    quantidades, valores = ler_arquivo_csv(nome_arquivo)
    produto_mais_vendido, valor_total_geral = calcular_resumo(quantidades, valores)
    exibir_relatorio(quantidades, valores, produto_mais_vendido, valor_total_geral)

if __name__ == "__main__":
    main()
