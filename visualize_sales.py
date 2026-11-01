import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("exports", exist_ok=True)
conn = sqlite3.connect("data/sales_database.db")

# 1. Load Raw Joined Sales Data into Pandas
query = """
SELECT 
    o.order_id,
    o.order_date,
    c.name AS customer_name,
    p.product_name,
    p.category,
    p.price,
    oi.quantity,
    oi.discount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status = 'Completed';
"""

df = pd.read_sql_query(query, conn)
conn.close()

# 2. Pandas Data Cleaning & Feature Engineering
df.dropna(inplace=True)
df['order_date'] = pd.to_datetime(df['order_date'])
df['net_revenue'] = (df['price'] * df['quantity'] * (1 - df['discount'])).round(2)
df['order_month'] = df['order_date'].dt.strftime('%Y-%m')

# 3. Print Key Business Insights
print("=== BUSINESS INSIGHTS SUMMARY ===")
print(f"Total Revenue: ${df['net_revenue'].sum():,.2f}")
print(f"Total Units Sold: {df['quantity'].sum()}")
print(f"Top Selling Product: {df.groupby('product_name')['net_revenue'].sum().idxmax()}")

# 4. Chart 1: Top-Selling Products Bar Chart
plt.figure(figsize=(8, 5))
top_products = df.groupby('product_name')['net_revenue'].sum().sort_values(ascending=False).reset_index()
sns.barplot(data=top_products, x='net_revenue', y='product_name', hue='product_name', palette='viridis', legend=False)
plt.title('Top-Selling Products by Revenue')
plt.xlabel('Total Revenue ($)')
plt.ylabel('Product Name')
plt.tight_layout()
plt.savefig('exports/top_products.png')
plt.close()

# 5. Chart 2: Monthly Sales Trend Line Chart
plt.figure(figsize=(8, 4))
monthly_sales = df.groupby('order_month')['net_revenue'].sum().reset_index()
sns.lineplot(data=monthly_sales, x='order_month', y='net_revenue', marker='o', linewidth=2.5, color='royalblue')
plt.title('Monthly Sales Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Revenue ($)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('exports/monthly_sales_trend.png')
plt.close()

print("Charts saved successfully inside the 'exports' folder!")