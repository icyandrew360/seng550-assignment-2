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

def process_customer(csv_line):
    current_date = datetime.now().strftime('%Y-%m-%d')
    customer_id, name, city = transform_customer_data(csv_line.split(','))
# Query the current customer data to check if this is a new customer or an update
    cursor.execute("""SELECT * FROM dim_customers WHERE customer_id = ? AND is_current = 1""", (customer_id))
    current_record = cursor.fetchone()
    if current_record:
        # Expire the old record
        cursor.execute("""UPDATE dim_customers SET is_current = 0, end_date = ? WHERE customer_id = ? AND is_current = 1""", (current_date, customer_id))
        # Insert the new record
        cursor.execute("""INSERT INTO dim_customers VALUES (?,?,?,?,?,?)""", (customer_id, name, city, current_date, None, 1))
    else:
        # New customer, insert into dim_customers
        cursor.execute("""INSERT INTO dim_customers VALUES (?,?,?,?,?,?)""", (customer_id, name, city, current_date, None, 1))
    conn.commit()

if __name__ == "__main__":
    while True:
# Simulate customer input from the command line in CSV format
        csv_input = input("Enter customer data (CSV format: customer_id,name,city): ")
# Process customer record
        process_customer(csv_input)