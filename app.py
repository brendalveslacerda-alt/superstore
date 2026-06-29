from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import os

app = Flask(__name__)


def init_db():
    """Cria o banco e a tabela apenas se ainda não existirem."""
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='products'"
    )
    existe = cursor.fetchone()

    if existe:
        conn.close()
        print("Banco já existe e está pronto.")
        return

    print("Criando banco de dados a partir do product.csv...")

    cursor.execute("""
        CREATE TABLE products (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id   TEXT UNIQUE NOT NULL,
            product_name TEXT NOT NULL,
            category     TEXT,
            sub_category TEXT
        )
    """)

    df = pd.read_csv("product.csv")
    df = df.drop_duplicates(subset=["Product ID"])

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO products
                (product_id, product_name, category, sub_category)
            VALUES (?, ?, ?, ?)
        """, (row["Product ID"], row["Product Name"],
              row["Category"], row["Sub-Category"]))

    conn.commit()
    conn.close()
    print(f"Banco criado com {len(df)} produtos.")


init_db()


def query_db(sql, args=()):
    conn = sqlite3.connect("products.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, args)
    result = cursor.fetchall()
    conn.close()
    return result


@app.route("/")
def index():
    search = request.args.get("q", "")
    category = request.args.get("cat", "")

    if search:
        products = query_db("""
            SELECT * FROM products
            WHERE product_name LIKE ?
               OR category LIKE ?
               OR sub_category LIKE ?
            ORDER BY category
        """, (f"%{search}%", f"%{search}%", f"%{search}%"))

    elif category:
        products = query_db("""
            SELECT * FROM products
            WHERE category = ?
            ORDER BY sub_category, product_name
        """, (category,))

    else:
        products = query_db("""
            SELECT * FROM products
            ORDER BY category, product_name
        """)

    categories = query_db(
        "SELECT DISTINCT category FROM products ORDER BY category"
    )

    return render_template("index.html",
                           products=products,
                           categories=categories,
                           search=search,
                           category=category)


@app.route("/product/<product_id>")
def detail(product_id):
    result = query_db(
        "SELECT * FROM products WHERE product_id = ?", (product_id,)
    )
    product = result[0] if result else None
    return render_template("produto.html", product=product)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

