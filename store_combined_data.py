import psycopg2
from fetch_customer_profile import fetch_customer_profile  # Import the function

def store_combined_data(combined_data):
    conn = psycopg2.connect(
        database="mydb",
        user="postgres",
        password="Admin@123",
        host="127.0.0.1",
        port="5432"
    )
    cursor = conn.cursor()

    create_combined_data_table_sql = """
    CREATE TABLE IF NOT EXISTS combined_data (
        id SERIAL PRIMARY KEY,
        cust_id_ VARCHAR(20),
        tran_id_ VARCHAR(50),
        tran_amount_ NUMERIC(10, 2),
        transaction_datetime_ TIMESTAMP,
        country VARCHAR(50),
        tran_count_ INT,
        last_tran_time TIMESTAMP
    );
    """
    cursor.execute(create_combined_data_table_sql)

    insert_combined_data_sql = """
    INSERT INTO combined_data (cust_id_, tran_id_, tran_amount_, transaction_datetime_, country, tran_count_, last_tran_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    profile = fetch_customer_profile(combined_data['inputs'][0]['value'])  # Extract profile using cust_id_
    combined_data_values = (
        combined_data['inputs'][0]['value'],
        combined_data['inputs'][3]['value'],
        combined_data['inputs'][1]['value'],
        combined_data['inputs'][4]['value'],
        combined_data['inputs'][2]['value'],
        profile['tran_count_'],
        profile['last_tran_time']
    )
    cursor.execute(insert_combined_data_sql, combined_data_values)
    conn.commit()
    cursor.close()
    conn.close()
