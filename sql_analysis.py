import sqlite3
import pandas as pd

conn = sqlite3.connect("data/sales_database.db")

# Query 1: Product Performance (Using JOIN, SUM, ROUND, and GROUP BY)
product_query = """
SELECT 
    p.category,
    p.product_name,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.quantity * p.price * (1 - oi.discount)), 2) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id
ORDER BY total_revenue DESC;
"""

print("=== 1. PRODUCT REVENUE & PERFORMANCE ===")
df_products = pd.read_sql_query(product_query, conn)
print(df_products.to_string(index=False))

# Query 2: Customer Purchasing Patterns (Using multiple JOINs, COUNT, and SUM)
customer_query = """
SELECT 
    c.customer_id,
    c.name AS customer_name,
    c.city,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.quantity * p.price * (1 - oi.discount)), 2) AS lifetime_spend
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY c.customer_id
ORDER BY lifetime_spend DESC;
"""

print("\n=== 2. CUSTOMER PURCHASING PATTERNS ===")
df_customers = pd.read_sql_query(customer_query, conn)
print(df_customers.to_string(index=False))

conn.close()