import psycopg2

def fetch_customer_profile(cust_id_):
    conn = psycopg2.connect(
        database="mydb",
        user="postgres",
        password="Admin@123",
        host="127.0.0.1",
        port="5432"
    )
    cursor = conn.cursor()

    fetch_query = """
    SELECT cust_id_, cust_name_, address, balance, tran_count_, last_tran_time 
    FROM customer_profile
    WHERE cust_id_ = %s;
    """
    cursor.execute(fetch_query, (cust_id_,))
    profile = cursor.fetchone()

    if profile:
        profile_dict = {
            'cust_id_': profile[0],
            'cust_name_': profile[1],
            'address': profile[2],
            'balance': profile[3],
            'tran_count_': profile[4],
            'last_tran_time': profile[5]
        }
        return profile_dict
    return None

    cursor.close()
    conn.close()
