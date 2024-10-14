import sqlite3
conn = None

try:
    conn = sqlite3.connect('assignment2.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS fact_orders')
    cursor.execute("""
                   CREATE TABLE fact_orders (
                   order_id INTEGER PRIMARY KEY,
                   customer_id INTEGER,
                   order_date TEXT,
                   amount REAL
                   )""")
    cursor.execute('DROP TABLE IF EXISTS dim_customers')
    cursor.execute("""
                   CREATE TABLE dim_customers (
                   customer_id INTEGER,
                   name TEXT,
                   city TEXT,
                   effective_date TEXT,
                   end_date TEXT,
                   is_current Integer
                   )""")
    ## is_current is a flag to indicate if the record is the current record for the customer (1 if current, 0 if not)
    # effective_date: the date the record became active
    # end_date: the date the record became inactive and replaced with newer record. if NULL, the record is current.

    conn.commit()

except sqlite3.Error as e:
    print(e)

finally:
    if conn:
        conn.close()
        print('Connection closed')