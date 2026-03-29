import requests
from config import BASE_URL, EMAIL, DEVICE_ID, SECURITY_CODE

def base_payload():
    return {
        "email": EMAIL,
        "deviceId": DEVICE_ID,
        "securityCode": SECURITY_CODE,
        "langId": 1
    }

# 📦 المنتجات
def get_products():
    url = BASE_URL + "/online/products"

    payload = base_payload()

    res = requests.post(url, data=payload)
    return res.json()

# 🔍 فحص المنتج
def check_product(product_id):
    data = get_products()

    for p in data.get("data", []):
        if str(p["id"]) == str(product_id):
            return p.get("inStock", False)

    return False

# 🛒 إنشاء طلب
def create_order(product_id):
    url = BASE_URL + "/online/create_order"

    payload = base_payload()
    payload.update({
        "productId": product_id,
        "quantity": 1
    })

    res = requests.post(url, data=payload)

    return res.json().get("data", {}).get("orderId")

# 📄 تفاصيل الطلب
def get_order_details(order_id):
    url = BASE_URL + "/online/orders/details"

    payload = base_payload()
    payload.update({
        "orderId": order_id
    })

    res = requests.post(url, data=payload)

    try:
        return res.json()["data"]["cards"][0]["code"]
    except:
        return None

# 💰 الرصيد
def check_balance():
    url = BASE_URL + "/online/check_balance"

    payload = base_payload()

    res = requests.post(url, data=payload)

    return res.json()
