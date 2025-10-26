import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()


def fetch_trans(id):
    # Hardcoded values
    API_KEY = os.getenv("NESSIE_KEY")
    BASE_URL = "http://api.nessieisreal.com"
    CUSTOMER_IDS = ["68d854ba9683f20dd5196bef", "68d854be9683f20dd5196c20", "68d854c29683f20dd5196c56"]
    CUSTOMER_ID = CUSTOMER_IDS[id]
    #Input the correct customer ID above
    # Get account id for customer
    account_url = f"{BASE_URL}/customers/{CUSTOMER_ID}/accounts?key={API_KEY}"
    account_response = requests.get(account_url)

    if account_response.status_code == 200:
        accounts = account_response.json()
        if accounts:
            ACCOUNT_ID = accounts[0]["_id"]   # ✅ use "_id", not "customer_id"
        else:
            raise ValueError("No accounts found for this customer")
    else:
        raise ValueError("Error fetching accounts:", account_response.text)

    # Build purchases endpoint URL
    url = f"{BASE_URL}/accounts/{ACCOUNT_ID}/purchases?key={API_KEY}"

    # Fetch purchases
    response = requests.get(url)

    if response.status_code == 200:
        purchases = response.json()
    else:
        # In case of error (like 404), still dump the error message
        purchases = {
            "account_id": ACCOUNT_ID,
            "status_code": response.status_code,
            "response": response.json()
        }

    for purchase in purchases:
        purchase['status'] = "executed"

    return purchases
