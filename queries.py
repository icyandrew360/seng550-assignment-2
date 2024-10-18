import sqlite3
from tabulate import tabulate
# Connect to SQLite
conn = sqlite3.connect('assignment2.db')
cursor = conn.cursor()

def get_city_order_details():
# Total amount of orders and total number of orders for each city
    cursor.execute('''
        SELECT c.city, COUNT(o.amount) as total_number, SUM(o.amount) as total_amount 
        FROM fact_orders o 
        LEFT JOIN dim_customers c 
        ON o.customer_id = c.customer_id 
        AND (
            (c.end_date IS NULL AND o.order_date > c.effective_date)
            OR
            (c.end_date IS NOT NULL AND o.order_date BETWEEN c.effective_date AND c.end_date)
        )    
        GROUP BY c.city  
    ''')

    result = cursor.fetchall()
    headers = [i[0] for i in cursor.description] # generate the labels from the cursor object
    print (tabulate(result, headers=headers, tablefmt="psql"))

def get_customer_total_orders():
    # Question answer: no, it does not. we are not using the customer name in the query so we have all the details we need in the fact_orders table.
    cursor.execute('''
        SELECT customer_id, COUNT(order_id) as total_orders
        FROM fact_orders
        GROUP BY customer_id
    ''')
    result = cursor.fetchall()
    headers = [i[0] for i in cursor.description] # generate the labels from the cursor object
    print (tabulate(result, headers=headers, tablefmt="psql"))

def get_order_amounts_by_customers_in_their_current_city_and_previous_city():
    # Total amount of orders for each customer in their current city and previous city
    cursor.execute('''
        SELECT o.customer_id,         
        SUM(CASE 
            WHEN c.end_date IS NULL AND o.order_date > c.effective_date THEN o.amount 
            ELSE 0 
        END) AS current_city_amount,
        SUM(CASE 
            WHEN c.end_date IS NOT NULL AND o.order_date BETWEEN c.effective_date AND c.end_date THEN o.amount 
            ELSE 0 
        END) AS previous_city_amount
        FROM fact_orders o LEFT JOIN 
            (SELECT * FROM dim_customers ORDER BY effective_date DESC LIMIT 2) c
        ON o.customer_id = c.customer_id 
        AND (
            (c.end_date IS NULL AND o.order_date > c.effective_date)
            OR
            (c.end_date IS NOT NULL AND o.order_date BETWEEN c.effective_date AND c.end_date)
        )   
    ''')
    result = cursor.fetchall()
    headers = [i[0] for i in cursor.description] # generate the labels from the cursor object
    print (tabulate(result, headers=headers, tablefmt="psql"))


get_order_amounts_by_customers_in_their_current_city_and_previous_city()

conn.close()