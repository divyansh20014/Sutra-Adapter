import requests
from fetch_customer_profile import fetch_customer_profile
from update_profile import update_customer_profile
from log_alerts import log_alert
from store_combined_data import store_combined_data
from datetime import datetime

def process_transaction(transaction):
    # Mock transaction data (use actual transaction values if available)
    mock_transactions = {
        'cust_id_': '123456789101112',
        'tran_id_': 'tran1',
        'tran_amount_': 3473.00,
        'transaction_datetime_': '2024-08-23T16:55:07',
        'country': 'USA'
    }
    
    # Replace transaction values with mock data for testing
    cust_id_ = transaction.get('cust_id_', mock_transactions['cust_id_'])
    tran_id_ = transaction.get('tran_id_', mock_transactions['tran_id_'])
    tran_amount_ = transaction.get('tran_amount_', mock_transactions['tran_amount_'])
    transaction_datetime_ = transaction.get('transaction_datetime_', mock_transactions['transaction_datetime_'])
    country = transaction.get('country', mock_transactions['country'])

    # Fetch customer profile
    profile = fetch_customer_profile(cust_id_)
    if not profile:
        return {"error": "Profile not found"}, 404

    # Update customer profile
    update_success = update_customer_profile(cust_id_, tran_amount_, transaction_datetime_)
    if not update_success:
        return {"error": "Profile update failed"}, 500

    # Combine transaction and profile data
    combined_data = {
        'inputs': [
            {"name": "cust_id_", "value": cust_id_},
            {"name": "tran_amount_", "value": tran_amount_},
            {"name": "tran_count_", "value": profile['tran_count_']},
            {"name": "tran_id_", "value": tran_id_},
            {"name": "transaction_datetime_", "value": transaction_datetime_}
        ]
    }

    # Send data to the rule set endpoint
    response = requests.post('https://sid-api-endpoint.com/ruleset', json=combined_data)
    if response.status_code == 200:
        alert_data = response.json()
        log_alert(alert_data)
        store_combined_data(combined_data)
        return alert_data, 200
    return {"error": "Failed to get response from ruleset endpoint"}, response.status_code
