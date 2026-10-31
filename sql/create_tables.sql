USE varejo_favorita;

DROP TABLE IF EXISTS fato_vendas;
DROP TABLE IF EXISTS fato_transacoes;
DROP TABLE IF EXISTS dim_loja;
DROP TABLE IF EXISTS dim_familia;
DROP TABLE IF EXISTS dim_calendario;

CREATE TABLE dim_loja (
    id_loja       INT PRIMARY KEY,
    cidade        VARCHAR(50) NOT NULL,
    estado        VARCHAR(50) NOT NULL,
    tipo_loja     CHAR(1)     NOT NULL,
    cluster_loja  INT         NOT NULL
);

CREATE TABLE dim_familia (
    id_familia    INT AUTO_INCREMENT PRIMARY KEY,
    nome_familia  VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE dim_calendario (
    data              DATE PRIMARY KEY,
    ano               SMALLINT    NOT NULL,
    trimestre         TINYINT     NOT NULL,
    mes               TINYINT     NOT NULL,
    nome_mes          VARCHAR(15) NOT NULL,
    dia_semana        VARCHAR(15) NOT NULL,
    fim_de_semana     BOOLEAN     NOT NULL,
    feriado_nacional  BOOLEAN     NOT NULL,
    preco_petroleo    DECIMAL(8,2)
);

CREATE TABLE fato_vendas (
    data            DATE          NOT NULL,
    id_loja         INT           NOT NULL,
    id_familia      INT           NOT NULL,
    vendas          DECIMAL(12,3) NOT NULL,
    itens_promocao  INT           NOT NULL,
    PRIMARY KEY (data, id_loja, id_familia),
    FOREIGN KEY (data)       REFERENCES dim_calendario(data),
    FOREIGN KEY (id_loja)    REFERENCES dim_loja(id_loja),
    FOREIGN KEY (id_familia) REFERENCES dim_familia(id_familia)
);

CREATE TABLE fato_transacoes (
    data        DATE NOT NULL,
    id_loja     INT  NOT NULL,
    transacoes  INT  NOT NULL,
    PRIMARY KEY (data, id_loja),
    FOREIGN KEY (data)    REFERENCES dim_calendario(data),
    FOREIGN KEY (id_loja) REFERENCES dim_loja(id_loja)
);