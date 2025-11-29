import httpx
import uuid

API_URL = "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2"

# Llaves correctas para Webpay REST (Integración)
API_KEY_ID = "597055555532"
API_KEY_SECRET = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"

headers = {
    "Tbk-Api-Key-Id": API_KEY_ID,
    "Tbk-Api-Key-Secret": API_KEY_SECRET,
    "Content-Type": "application/json",
    "Accept": "application/json"
}


async def iniciar_transaccion(buy_order: str, amount: float, return_url: str):

    session_id = str(uuid.uuid4())

    payload = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(f"{API_URL}/transactions", json=payload, headers=headers)

    if res.status_code != 200:
        raise Exception(f"Error Webpay al iniciar transacción: {res.text}")

    data = res.json()
    return data["token"], data["url"]


async def confirmar_transaccion(token: str):
    async with httpx.AsyncClient() as client:
        res = await client.put(f"{API_URL}/transactions/{token}", headers=headers)

    if res.status_code != 200:
        raise Exception(f"Error Webpay al confirmar: {res.text}")

    return res.json()

