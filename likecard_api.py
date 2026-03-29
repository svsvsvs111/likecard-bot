import requests
import hashlib
import time
from config import BASE_URL, API_KEY, SECRET

def generate_headers():
    timestamp = str(int(time.time()))
    raw = API_KEY + timestamp + SECRET
    signature = hashlib.sha256(raw.encode()).hexdigest()

    return {
        "apiKey": API_KEY,
        "time": timestamp,
        "signature": signature,
        "Content-Type": "application/json"
    }

def get_products():
    res = requests.post(BASE_URL + "/online/products", headers=generate_headers())
    return res.json()

def check_product(product_id):
    data = get_products()
    for p in data.get("data", []):
        if p["id"] == product_id:
            return p.get("inStock", False)
    return False

def create_order(product_id):
    res = requests.post(
        BASE_URL + "/online/create_order",
        json={"productId": product_id, "quantity": 1},
        headers=generate_headers()
    )
    return res.json().get("data", {}).get("orderId")

def get_order_details(order_id):
    res = requests.post(
        BASE_URL + "/online/orders/details",
        json={"orderId": order_id},
        headers=generate_headers()
    )

    try:
        return res.json()["data"]["cards"][0]["code"]
    except:
        return None

def check_balance():
    res = requests.post(BASE_URL + "/online/check_balance", headers=generate_headers())
    return res.json()
