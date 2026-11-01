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


if __name__ == "__main__":
    from extract import extrair_dados

    dados = extrair_dados()
    dim_loja = transformar_dim_loja(dados["stores"])
    dim_familia = transformar_dim_familia(dados["train"])
    dim_calendario = transformar_dim_calendario(dados["train"], dados["oil"], dados["holidays"])

    print("dim_loja:", dim_loja.shape)
    print("dim_familia:", dim_familia.shape)
    print("dim_calendario:", dim_calendario.shape)
    print("Feriados nacionais:", dim_calendario["feriado_nacional"].sum())
    print("Preços de petróleo vazios:", dim_calendario["preco_petroleo"].isnull().sum())
    print(dim_calendario.head(8))