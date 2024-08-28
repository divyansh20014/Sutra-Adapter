import psycopg2
from datetime import datetime

def update_customer_profile(cust_id_, tran_count_, transaction_datetime_):
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        database="mydb",
        user="postgres",
        password="Admin@123",
        host="127.0.0.1",
        port="5432"
    )
    cursor = conn.cursor()

    # Fetch current profile details
    cursor.execute("SELECT tran_count_, last_tran_time FROM customer_profile WHERE cust_id_ = %s", (cust_id_,))
    result = cursor.fetchone()

    if result:
        tran_count_, last_tran_time = result
        last_tran_time = last_tran_time or datetime(1970, 1, 1)  # Handle null values

        # Calculate time difference in minutes
        time_diff = (transaction_datetime_ - last_tran_time).total_seconds() / 60.0

        if time_diff < 20:
            tran_count_ += 1
        else:
            tran_count_ = 1
            last_tran_time = transaction_datetime_

        # Update profile in the database
        update_sql = """
        UPDATE customer_profile
        SET tran_count_ = %s, last_tran_time = %s
        WHERE cust_id_ = %s
        """
        cursor.execute(update_sql, (tran_count_, last_tran_time, cust_id_))

        conn.commit()

    cursor.close()
    conn.close()



# import psycopg2
# from datetime import datetime
# from fetch_customer_profile import fetch_customer_profile

# def update_profile(cust_id_, transaction_datetime_):
#     conn = psycopg2.connect(
#         database="mydb",
#         user="postgres",
#         password="Admin@123",
#         host="127.0.0.1",
#         port="5432"
#     )
#     cursor = conn.cursor()

#     profile = fetch_customer_profile(cust_id_)

#     if profile:
#         last_tran_time = profile['last_tran_time']
#         tran_count_ = profile['tran_count_']

#         if last_tran_time and (transaction_datetime_ - last_tran_time).total_seconds() < 20 * 60:
#             tran_count_ += 1
#         else:
#             tran_count_ = 1

#         update_query = """
#         UPDATE customer_profile
#         SET tran_count_ = %s, last_tran_time = %s
#         WHERE cust_id_ = %s;
#         """
#         cursor.execute(update_query, (tran_count_, transaction_datetime_, cust_id_))
#         conn.commit()

#     cursor.close()
#     conn.close()
