import time

from conexao import criar_engine
from extract import extrair_dados
from transform import (transformar_dim_loja, transformar_dim_familia,
                       transformar_dim_calendario, transformar_fato_vendas,
                       transformar_fato_transacoes)
from load import limpar_tabelas, carregar_tabelas


def main():
    inicio = time.time()

    print("1/3 Extraindo dados...")
    dados = extrair_dados()

    print("2/3 Transformando dados...")
    dim_familia = transformar_dim_familia(dados["train"])
    tabelas = {
        "dim_loja": transformar_dim_loja(dados["stores"]),
        "dim_familia": dim_familia,
        "dim_calendario": transformar_dim_calendario(
            dados["train"], dados["oil"], dados["holidays"]),
        "fato_vendas": transformar_fato_vendas(dados["train"], dim_familia),
        "fato_transacoes": transformar_fato_transacoes(dados["transactions"]),
    }

    print("3/3 Carregando no MySQL...")
    engine = criar_engine()
    limpar_tabelas(engine)
    carregar_tabelas(engine, tabelas)

    print(f"\nPipeline concluído em {time.time() - inicio:.0f} segundos.")


if __name__ == "__main__":
    main()