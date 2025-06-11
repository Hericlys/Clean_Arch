import requests

url = "http://localhost:5000/order"

payload = {
    "client": "Hericlys",
    "items": [
        {"name": "Teclado", "price": 150},
        {"name": "Mouse", "price": 100}
    ]
}

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print("Status:", response.status_code)
print("Resposta bruta:", response.text)

try:
    json_data = response.json()
    print("JSON decodificado:", json_data)
except Exception as e:
    print("❌ Não foi possível decodificar JSON:", e)
