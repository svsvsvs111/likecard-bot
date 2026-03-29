import sqlite3

conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    product_name TEXT,
    active INTEGER DEFAULT 1
)
""")

conn.commit()

def add_subscription(user_id, product_id, product_name):
    cursor.execute("""
    SELECT * FROM subscriptions 
    WHERE user_id=? AND product_id=? AND active=1
    """, (user_id, product_id))

    if cursor.fetchone():
        return False

    cursor.execute("""
    INSERT INTO subscriptions (user_id, product_id, product_name) 
    VALUES (?, ?, ?)
    """, (user_id, product_id, product_name))

    conn.commit()
    return True

def get_subscriptions():
    cursor.execute("SELECT * FROM subscriptions WHERE active=1")
    return cursor.fetchall()

def deactivate_subscription(sub_id):
    cursor.execute("UPDATE subscriptions SET active=0 WHERE id=?", (sub_id,))
    conn.commit()
