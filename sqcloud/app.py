from flask import Flask, render_template, request
import sqlite3 

app = Flask(__name__)

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
    search = request.args.get("q","")
    category = request.args.get("cat","")
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
            """, (category))
    else:
        products = query_db("""
            SELECT * FROM products
            ORDER BY category, product_name
            """)                                    
    categories = query_db("SELECT DISTINCT category FROM products ORDER BY category")
    return render_template("index.html",
                   products=products,
                   categories=categories,
                   search=search,
                   category=category)

@app.route("/product/<product_id>")
def detail(product_id):
    product = query_db("""
        SELECT * FROM products WHERE product_id = ?
        """, (product_id))
    
if __name__ == "__main__":
    app.run(debug=True)