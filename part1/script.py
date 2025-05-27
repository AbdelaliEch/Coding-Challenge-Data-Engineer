import psycopg2
import time
from dotenv import load_dotenv
import os

# Function to execute a query and measure its execution time
def execute_query(query):
    start_time = time.time()

    cursor.execute(query)

    end_time = time.time()

    # Uncomment the lines below to fetch and print the results of the query
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)

    execution_time = end_time - start_time
    return f"Execution time: {execution_time:.5f} seconds"



# Load sensitive info from environment variables
load_dotenv()
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(
        host="localhost",
        database=db_name,
        user=db_user,
        password=db_password,
        port="5432"
    )
except Exception as e:
    print(f"Could not connect to the database")
    exit(1)

# Create a cursor object
cursor = conn.cursor()


query1 = """
    SELECT 
        dates.date, 
        COUNT(DISTINCT(events.user_id)) AS "Rolling Weekly active users"
    FROM dates LEFT JOIN events 
    ON 
        events.timestamp::date <= dates.date 
    AND 
        events.timestamp::date > (dates.date - INTERVAL '7 days')
    GROUP BY 
        dates.date
    ORDER BY 
        dates.date;
"""

query2 = """
    SELECT 
        dates.date AS "End of the week", 
        COUNT(DISTINCT(events.user_id)) AS "Weekly active users"
    FROM 
        dates 
    LEFT JOIN 
        events 
    ON 
        events.timestamp::date <= dates.date 
    AND 
        events.timestamp::date > (dates.date - INTERVAL '7 days')
    WHERE 
        extract(dow from dates.date) = 0
    GROUP BY 
        dates.date
    ORDER BY 
        dates.date;
"""

query3 = """
    SELECT 
        category, 
        SUM(price::numeric(10, 2)) AS "Revenue per category"
    FROM 
        events 
    LEFT JOIN 
        products 
    ON 
        events.product_id = products.product_id
    WHERE 
        event_type = 'purchased'
    GROUP BY 
        category
    ORDER BY 
        "Revenue per category" DESC;
"""


# Create dates table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS dates AS 
    SELECT DATE(
        generate_series('2025-01-01'::date, '2025-12-31'::date, '1 day'::interval)
    ) AS date;
""")
conn.commit()


# Execute Weekly Active Users queries before indexing
# Rolling 7-day Weekly Active Users query
print(f"RWAU query execution time Before indexing:\n  {execute_query(query1)}")
# Calendar Weekly Active Users query
print(f"CWAU query execution time Before indexing:\n  {execute_query(query2)}")

# Create indexes to optimize the Weekly Active Users queries
cursor.execute("""CREATE INDEX IF NOT EXISTS events_timestamp_date_index ON events ((timestamp::date), user_id);""")
conn.commit()

# Execute Weekly Active Users queries after indexing
# Rolling 7-day Weekly Active Users query
print(f"RWAU query execution time After indexing:\n  {execute_query(query1)}")
# Calendar Weekly Active Users query
print(f"CWAU query execution time After indexing:\n  {execute_query(query2)}")



# Execute Revenue per Category query before indexing
print(f"RPC query execution time before indexing:\n  {execute_query(query3)}")

# Create indexes to optimize the Revenue per Category query
cursor.execute("""CREATE INDEX IF NOT EXISTS events_eventtype_productid_index ON events (event_type, product_id);""")
cursor.execute("""CREATE INDEX IF NOT EXISTS products_product_id_index ON products (product_id);""")
conn.commit()

# Execute Revenue per Category query after indexing
print(f"RPC query execution time after indexing:\n  {execute_query(query3)}")



cursor.close()
conn.close()