import psycopg2

def log_alert(alert_data):
    conn = psycopg2.connect(
        database="mydb",
        user="postgres",
        password="Admin@123",
        host="127.0.0.1",
        port="5432"
    )
    cursor = conn.cursor()

    create_alert_table_sql = """
    CREATE TABLE IF NOT EXISTS alerts (
        alert_id SERIAL PRIMARY KEY,
        cust_id_ VARCHAR(20),
        tran_id_ VARCHAR(50),
        alert_flag FLOAT,
        rule_id VARCHAR(50),
        rule_score FLOAT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_alert_table_sql)

    insert_alert_sql = """
    INSERT INTO alerts (cust_id_, tran_id_, alert_flag, rule_id, rule_score)
    VALUES (%s, %s, %s, %s, %s);
    """
    alert_entries = [
        (
            alert_data.get('cust_id'),
            alert_data.get('tran_id'),
            alert_data.get('alert_flag'),
            alert_data.get('rule_id'),
            alert_data.get('rule_score')
        )
    ]
    cursor.executemany(insert_alert_sql, alert_entries)
    conn.commit()
    cursor.close()
    conn.close()
