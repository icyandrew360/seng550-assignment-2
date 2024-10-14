import sqlite3
from tabulate import tabulate
# Connect to SQLite
conn = sqlite3.connect('assignment2.db')
cursor = conn.cursor()

#
cursor.execute('''
    SELECT c.city, SUM(o.amount) as total_amount 
    FROM fact_orders o 
    LEFT JOIN dim_customers c 
    ON o.customer_id = c.customer_id 
    AND (
        (c.end_date IS NULL AND o.order_date >= c.effective_date)
        OR
        (c.end_date IS NOT NULL AND o.order_date BETWEEN c.effective_date AND c.end_date)
    )    
    GROUP BY c.city  
''')
    # AND (
    #     (c.end_date IS NOT NULL AND o.order_date BETWEEN c.effective_date AND c.end_date) 
    #     OR 
    #     (c.end_date IS NULL AND o.order_date > c.effective_date)
    # ) 
result = cursor.fetchone()
print (result)