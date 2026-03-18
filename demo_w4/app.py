from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "Ho Quy Ly", "author": "Nguyen Xuan Khanh", "publishedYear": 2000},
    {"id": 2, "title": "Thuong nho muoi hai", "author": "Vu Bang", "publishedYear": 1960},
    {"id": 3, "title": "Gio dau mua", "author": "Thach Lam", "publishedYear": 1937}
]

current_id = 4


def api_response(data=None, message="Success", status=200, error=None):
    return jsonify({
        "status": status,
        "message": message,
        "data": data,
        "error": error,
    }), status


@app.route('/api/v1/books', methods=['GET'])
def get_books():
    return api_response(data=books)


@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return api_response(data=book)
    return api_response(message="Book not found", status=404, error="NOT_FOUND")


@app.route('/api/v1/books', methods=['POST'])
def create_book():
    global current_id
    data = request.get_json()

    if not data or not data.get("title") or not data.get("author"):
        return api_response(message="Invalid input", status=400, error="BAD_REQUEST")

    new_book = {
        "id": current_id,
        "title": data["title"],
        "author": data["author"],
        "publishedYear": data.get("publishedYear")
    }

    books.append(new_book)
    current_id += 1

    return api_response(data=new_book, message="Created", status=201)


@app.route('/api/v1/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = next((b for b in books if b["id"] == book_id), None)

    if book:
        book.update({
            "title": data.get("title", book["title"]),
            "author": data.get("author", book["author"]),
            "publishedYear": data.get("publishedYear", book["publishedYear"])
        })
        return api_response(data=book, message="Updated")

    return api_response(message="Book not found", status=404, error="NOT_FOUND")


@app.route('/api/v1/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    initial_length = len(books)
    books = [b for b in books if b["id"] != book_id]

    if len(books) < initial_length:
        return api_response(message="Deleted", status=200)

    return api_response(message="Book not found", status=404, error="NOT_FOUND")


if __name__ == '__main__':
    app.run(debug=True, port=5000)