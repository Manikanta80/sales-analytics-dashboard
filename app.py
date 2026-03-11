from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mani123456789",
    database="salesdb"
)

# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# DASHBOARD KPI
@app.route("/dashboard")
def dashboard():
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
        SUM(p.selling_price * s.quantity) AS total_revenue,
        SUM((p.selling_price - p.cost_price) * s.quantity) AS total_profit
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
    """)

    data = cursor.fetchone()

    return jsonify({
        "total_revenue": float(data["total_revenue"]),
        "total_profit": float(data["total_profit"])
    })


# TOP STORES
@app.route("/topstores")
def top_stores():
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
        st.store_name,
        SUM(p.selling_price * s.quantity) AS revenue
        FROM sales s
        JOIN stores st ON s.store_id = st.store_id
        JOIN products p ON s.product_id = p.product_id
        GROUP BY st.store_name
        ORDER BY revenue DESC
        LIMIT 5
    """)

    data = cursor.fetchall()

    for row in data:
        row["revenue"] = float(row["revenue"])

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)