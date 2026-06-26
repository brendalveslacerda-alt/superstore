# Superstore — Cadastro de Produtos com Python e SQLite

Projeto de estudo para leitura de dados de vendas em CSV, extração de produtos únicos e criação de um banco de dados local com SQLite3.

## Tecnologias

- Python 3.14
- pandas
- sqlite3 (nativo do Python)

## Estrutura do projeto

python_sqlite3/
│
├── product.csv       # Arquivo de dados original
├── main.py           # Script principal
├── products.db       # Banco de dados gerado (criado ao rodar o script)
└── README.md         # Este arquivo

## Como executar

**1. Clone o repositório**
bash
git clone [github.com](https://github.com/seu-usuario/superstore.git)
cd superstore/python_sqlite3


**2. Instale as dependências**
bash
pip3 install pandas openpyxl (Em ambiente MacOS)


**3. Execute o script**
bash
python3 main.py (Em ambiente MacOS)


## O que o script faz

1. Lê o arquivo `product.csv` com pandas
2. Remove duplicatas no campo `Product ID`
3. Cria o banco de dados `products.db` com SQLite3
4. Insere os produtos únicos na tabela `products`
5. Exibe um resumo por categoria no terminal

## Estrutura do banco de dados

**Tabela: `products`**

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | Chave primária auto-incrementada |
| product_id | TEXT | Identificador único do produto (ex: FUR-BO-10001798) |
| product_name | TEXT | Nome completo do produto |
| category | TEXT | Categoria (Furniture, Technology, Office Supplies) |
| sub_category | TEXT | Subcategoria (Chairs, Phones, Paper...) |

## Exemplo de consulta

```python
import sqlite3

conn = sqlite3.connect("products.db")
cursor = conn.cursor()

# Buscar produto por ID
cursor.execute("SELECT * FROM products WHERE product_id = ?", ("FUR-BO-10001798",))
print(cursor.fetchone())

# Listar todos os produtos de uma categoria
cursor.execute("SELECT product_name FROM products WHERE category = 'Technology'")
for row in cursor.fetchall():
    print(row)

conn.close()
```

## Aprendizados

- Leitura de CSV com `pandas`
- Remoção de duplicatas com `drop_duplicates()`
- Criação de tabelas no SQLite com constraints `UNIQUE`
- Inserção segura com `INSERT OR IGNORE` e placeholders `?`
