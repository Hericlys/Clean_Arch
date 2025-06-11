from flask import Flask, request, jsonify
from interface import repository
from use_cases.new_order import new_order
from adapters.repository_factory import get_repository


app = Flask(__name__)

try:
    repository = get_repository('sqllite')
except Exception as e:
    print(e)
    print('🔃 Setting repository for memory type')
    repository = get_repository()
    print('✅Repository type set to memory')


@app.route("/order", methods=["POST"])
def new():
    data = request.get_json()

    client = data.get('client')
    items = data.get('items', [])

    if not client or not items:
        return jsonify({'erro': 'Client and items are required'})
    
    order = new_order(client, items, repository)

    return jsonify({
        "client": order.client,
        "items": [{'name': i.name, 'price': i.price} for i in order.items],
        "total": order.calculate_total()
    })

if __name__ == "__main__":
    app.run(debug=True)
