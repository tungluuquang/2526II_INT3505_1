from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {
        "id": 1,
        "name": "Alice",
        "status": "active",
        "email": "aliceinwonderland@gmail.com",
        "address": {
            "city": "Paris",
            "district": "34 Saint Germain"
        }
    },
    {
        "id": 2,
        "name": "Bob",
        "status": "inactive",
        "email": "bobbygang@gmail.com",
        "address": {
            "city": "Hanoi",
            "district": "Dong Da"
        }
    },
    {
        "id": 3,
        "name": "Charlie",
        "status": "active",
        "email": "charlieputh@gmail.com",
        "address": {
            "city": "HCM",
            "district": "District 1"
        }
    }
]

def api_response(data=None, message="Success", status=200, error=None):
    return jsonify({
        "status": status,
        "message": message,
        "data": data,
        "error": error
    }), status


# helper function for extensibility
def filter_fields(data, fields):
    if not fields:
        return data

    field_list = fields.split(",")

    filtered = []
    for item in data:
        filtered.append({k: v for k, v in item.items() if k in field_list})

    return filtered


# false — no versioning
# address returned as string
@app.route("/api/users", methods=["GET"])
def users_no_version():

    users_data = [
        {
            "id": u["id"],
            "name": u["name"],
            "status": u["status"],
            "email": u["email"],
            "address": f'{u["address"]["city"]}, {u["address"]["district"]}'
        }
        for u in users
    ]

    fields = request.args.get("fields")
    result = filter_fields(users_data, fields)

    return api_response(data=result)


# API version 1
# address is still a string
@app.route("/api/v1/users", methods=["GET"])
def users_v1():

    users_v1_data = [
        {
            "id": u["id"],
            "name": u["name"],
            "status": u["status"],
            "email": u["email"],
            "address": f'{u["address"]["city"]}, {u["address"]["district"]}'
        }
        for u in users
    ]

    fields = request.args.get("fields")
    result = filter_fields(users_v1_data, fields)

    return api_response(data=result)


# API version 2 (extensibility)
# address changed to object to support filtering
@app.route("/api/v2/users", methods=["GET"])
def users_v3():

    city = request.args.get("city")
    district = request.args.get("district")

    result = users

    if city:
        result = [u for u in result if u["address"]["city"].lower() == city.lower()]

    if district:
        result = [u for u in result if u["address"]["district"].lower() == district.lower()]

    fields = request.args.get("fields")
    result = filter_fields(result, fields)

    return api_response(data=result)


if __name__ == "__main__":
    app.run(debug=True)