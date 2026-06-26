import pandas as pd
import sqlite3

# LER O CSV
df = pd.read_csv("product.csv")
print(f"Registros carregados: {len(df)}")
print(df.columns.tolist())  # confirma os nomes exatos das colunas
print(df.head())

# PRODUTOS ÚNICOS 
produtos_unicos = df.drop_duplicates(subset=["Product ID"])
print(f"Produtos únicos: {len(produtos_unicos)}")

# BANCO DE DADOS
conn = sqlite3.connect("products.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS products")
cursor.execute("""
    CREATE TABLE products (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id   TEXT UNIQUE NOT NULL,
        product_name TEXT NOT NULL,
        category     TEXT,
        sub_category TEXT
    )
""")
conn.commit()

# INSERIR DADOS
for _, row in produtos_unicos.iterrows():
    cursor.execute("""
        INSERT OR IGNORE INTO products (product_id, product_name, category, sub_category)
        VALUES (?, ?, ?, ?)
    """, (
        row["Product ID"],
        row["Product Name"],
        row["Category"],
        row["Sub-Category"]
    ))
conn.commit()
print("Banco criado com sucesso.")

# CONSULTAS
cursor.execute("SELECT COUNT(*) FROM products")
total = cursor.fetchone()[0]
print(f"Total de produtos no banco: {total}")
cursor.execute("""
    SELECT category, COUNT(*) as total
    FROM products
    GROUP BY category
    ORDER BY total DESC
""")
print("\nProdutos por categoria:")
for cat, total in cursor.fetchall():
    print(f"  {cat}: {total}")
conn.close()