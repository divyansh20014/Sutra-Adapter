import psycopg2

def create_customer_profile_table():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        database="mydb",
        user="postgres",
        password="Admin@123",
        host="127.0.0.1",
        port="5432"
    )
    cursor = conn.cursor()

    # Create table SQL
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS customer_profile (
        cust_id_ SERIAL PRIMARY KEY,
        cust_name_ VARCHAR(100) NOT NULL,
        address TEXT,
        balance NUMERIC(10, 2),
        tran_count_ INT,
        last_tran_time TIMESTAMP
    );
    """
    
    # Execute the SQL command to create the table
    cursor.execute(create_table_sql)
    conn.commit()
    print("Customer profile table created successfully.")

    # Insert 5 specific entries with fixed last_tran_time
    insert_sql = """
    INSERT INTO customer_profile (
        cust_name_, address, balance, tran_count_, last_tran_time
    ) VALUES (%s, %s, %s, %s, %s);
    """
    
    entries = [
        ("John Doe", "123 Elm St, Springfield", 1500.00, 3, "2024-08-23 10:30:00"),
        ("Jane Smith", "456 Oak St, Springfield", 2200.00, 2, "2024-08-23 10:50:00"),
        ("Alice Johnson", "789 Pine St, Springfield", 5000.00, 1, "2024-08-23 11:00:00"),
        ("Bob Brown", "101 Maple St, Springfield", 800.00, 4, "2024-08-23 11:20:00"),
        ("Charlie Davis", "202 Birch St, Springfield", 3000.00, 9, "2024-08-23 11:40:00")
    ]
    
    for entry in entries:
        cursor.execute(insert_sql, entry)

    conn.commit()
    print("5 specific entries inserted successfully.")

    # Close the connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_customer_profile_table()
