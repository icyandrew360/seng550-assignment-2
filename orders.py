import sqlite3
from datetime import datetime
# Connect to SQLite
conn = sqlite3.connect('assignment2.db')
cursor = conn.cursor()

def transform_customer_data(data):
    clean_data = []
    for item in data:
        clean_data.append(item.strip())
    return clean_data

def process_order(csv_line):
    order_date = datetime.now().strftime('%Y-%m-%d')
    order_id, customer_id, amount = transform_customer_data(csv_line.split(','))
    # Insert the order into fact_orders
    cursor.execute("""INSERT INTO fact_orders VALUES (?,?,?,?)""", (order_id, customer_id, order_date, amount))
    conn.commit()
if __name__ == "__main__":

    while True:
    # Simulate order input from command line in CSV format
        csv_input = input("Enter order data (CSV format: order_id,customer_id,amount): ")
        # Process order record
        process_order(csv_input)