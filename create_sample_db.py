import os
import sqlite3

os.makedirs("sample_db", exist_ok=True)
DB = "sample_db/sample.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS customers (
  id INTEGER PRIMARY KEY,
  name TEXT,
  email TEXT,
  created_at TEXT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER,
  total_amount REAL,
  status TEXT,
  created_at TEXT,
  notes TEXT,
  FOREIGN KEY(customer_id) REFERENCES customers(id)
);
""")
# seed data
customers = [
    (1, "Alice Johnson", "alice@example.com", "2024-12-01"),
    (2, "Bob Lee", "bob@example.com", "2024-12-05"),
    (3, "Carol Singh", "carol@example.com", "2024-12-10"),
    (4, "David Kim", "david.kim@example.com", "2024-12-12"),
]

orders = [
    (1, 1, 120.50, "completed", "2025-01-03", "First order"),
    (2, 1, 15.00, "pending", "2025-01-07", "Gift wrap"),
    (3, 2, 250.00, "completed", "2025-02-10", "Bulk order"),
]

cur.executemany("INSERT OR REPLACE INTO customers VALUES (?,?,?,?)", customers)
cur.executemany("INSERT OR REPLACE INTO orders VALUES (?,?,?,?,?,?)", orders)
conn.commit()
conn.close()
print("Sample database created.")