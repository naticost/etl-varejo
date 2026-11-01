from sqlalchemy import text

ORDEM_CARGA = ["dim_loja", "dim_familia", "dim_calendario",
               "fato_vendas", "fato_transacoes"]


def limpar_tabelas(engine):
    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        for tabela in reversed(ORDEM_CARGA):
            conn.execute(text(f"TRUNCATE TABLE {tabela}"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))


def carregar_tabelas(engine, tabelas):
    for nome in ORDEM_CARGA:
        df = tabelas[nome]
        print(f"  Carregando {nome} ({len(df):,} linhas)...")
        df.to_sql(nome, engine, if_exists="append", index=False,
                  chunksize=5000, method="multi")