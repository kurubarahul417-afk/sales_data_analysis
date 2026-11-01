import os
import sqlite3

os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("data/sales_database.db")
cursor = conn.cursor()

# 1. Create Tables
cursor.executescript("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT,
    state TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE NOT NULL,
    status TEXT DEFAULT 'Completed',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    discount REAL DEFAULT 0.0,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")

# 2. Insert Sample Sales Records
cursor.executescript("""
INSERT OR IGNORE INTO customers VALUES 
(1, 'Alice Smith', 'Seattle', 'WA'),
(2, 'Bob Jones', 'Austin', 'TX'),
(3, 'Charlie Brown', 'Denver', 'CO'),
(4, 'Diana Prince', 'New York', 'NY');

INSERT OR IGNORE INTO products VALUES 
(101, 'Mechanical Keyboard', 'Electronics', 85.00),
(102, 'Ergonomic Mouse', 'Electronics', 45.00),
(103, 'Desk Mat XXL', 'Accessories', 25.00),
(104, 'Monitor Stand', 'Accessories', 35.00),
(105, 'USB-C Dock', 'Electronics', 110.00);

INSERT OR IGNORE INTO orders VALUES 
(1001, 1, '2026-01-15', 'Completed'),
(1002, 2, '2026-01-20', 'Completed'),
(1003, 1, '2026-02-05', 'Completed'),
(1004, 3, '2026-02-18', 'Completed'),
(1005, 4, '2026-03-02', 'Completed'),
(1006, 2, '2026-03-12', 'Completed');

INSERT OR IGNORE INTO order_items (order_id, product_id, quantity, discount) VALUES 
(1001, 101, 1, 0.05),
(1001, 103, 2, 0.0),
(1002, 102, 1, 0.0),
(1003, 105, 1, 0.10),
(1003, 104, 1, 0.0),
(1004, 101, 2, 0.0),
(1005, 102, 2, 0.0),
(1005, 105, 1, 0.15),
(1006, 103, 3, 0.05);
""")

conn.commit()
conn.close()
print("Database created and populated successfully!")