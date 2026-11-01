import pandas as pd

MESES = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio",
         6: "Junho", 7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro",
         11: "Novembro", 12: "Dezembro"}
DIAS = {0: "Segunda", 1: "Terça", 2: "Quarta", 3: "Quinta",
        4: "Sexta", 5: "Sábado", 6: "Domingo"}


def transformar_dim_loja(stores):
    return stores.rename(columns={
        "store_nbr": "id_loja", "city": "cidade", "state": "estado",
        "type": "tipo_loja", "cluster": "cluster_loja",
    })


def transformar_dim_familia(train):
    familias = sorted(train["family"].unique())
    return pd.DataFrame({
        "id_familia": range(1, len(familias) + 1),
        "nome_familia": familias,
    })


def transformar_dim_calendario(train, oil, holidays):
    datas = pd.date_range(train["date"].min(), train["date"].max())
    cal = pd.DataFrame({"data": datas})

    cal["ano"] = cal["data"].dt.year
    cal["trimestre"] = cal["data"].dt.quarter
    cal["mes"] = cal["data"].dt.month
    cal["nome_mes"] = cal["mes"].map(MESES)
    cal["dia_semana"] = cal["data"].dt.day_of_week.map(DIAS)
    cal["fim_de_semana"] = cal["data"].dt.day_of_week >= 5

    tipos_feriado = ["Holiday", "Transfer", "Additional", "Bridge"]
    nacionais = holidays[
        (holidays["locale"] == "National")
        & (holidays["type"].isin(tipos_feriado))
        & (~holidays["transferred"])
    ]
    cal["feriado_nacional"] = cal["data"].isin(nacionais["date"])

    petroleo = oil.set_index("date")["dcoilwtico"].reindex(datas).ffill()
    cal["preco_petroleo"] = petroleo.values

    return cal


def transformar_fato_vendas(train, dim_familia):
    abertura = train[train["sales"] > 0].groupby("store_nbr")["date"].min()
    vendas = train[train["date"] >= train["store_nbr"].map(abertura)]

    vendas = vendas.merge(dim_familia, left_on="family", right_on="nome_familia")
    vendas = vendas.rename(columns={
        "date": "data", "store_nbr": "id_loja",
        "sales": "vendas", "onpromotion": "itens_promocao",
    })
    return vendas[["data", "id_loja", "id_familia", "vendas", "itens_promocao"]]


def transformar_fato_transacoes(transactions):
    return transactions.rename(columns={
        "date": "data", "store_nbr": "id_loja", "transactions": "transacoes",
    })


if __name__ == "__main__":
    from extract import extrair_dados

    dados = extrair_dados()
    dim_familia = transformar_dim_familia(dados["train"])
    fato_vendas = transformar_fato_vendas(dados["train"], dim_familia)
    fato_transacoes = transformar_fato_transacoes(dados["transactions"])

    print(f"train original: {len(dados['train']):,} linhas")
    print(f"fato_vendas:    {len(fato_vendas):,} linhas")
    print(f"Linhas removidas: {len(dados['train']) - len(fato_vendas):,}")
    print(f"fato_transacoes: {len(fato_transacoes):,} linhas")

    print(f"\nTotal de vendas no train:       {dados['train']['sales'].sum():,.2f}")
    print(f"Total de vendas na fato_vendas: {fato_vendas['vendas'].sum():,.2f}")

    chave = ["data", "id_loja", "id_familia"]
    print("Linhas duplicadas na chave:", fato_vendas.duplicated(subset=chave).sum())