import uuid
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)

# ─── Swagger UI ───────────────────────────────────────────────
SWAGGER_URL = "/apidocs"
API_URL = "/api_doc.yaml"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Book Management API V2"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/api_doc.yaml")
def swagger_yaml():
    return send_from_directory(".", "api_doc.yaml")

# ─── In-memory DB ─────────────────────────────────────────────
books_db = {
    "1": {"id": "1", "title": "Ho Quy Ly",          "author": "Nguyen Xuan Khanh", "publishedYear": 2000},
    "2": {"id": "2", "title": "Thuong nho muoi hai", "author": "Vu Bang",           "publishedYear": 1960},
    "3": {"id": "3", "title": "Gio dau mua",         "author": "Thach Lam",         "publishedYear": 1937},
}

# ─── Helper ───────────────────────────────────────────────────
def api_response(data=None, message="Success", status=200, error=None):
    return jsonify({"status": status, "message": message, "data": data, "error": error}), status

# ─── Routes ───────────────────────────────────────────────────
@app.route("/")
def home():
    return jsonify({"message": "API is running", "swagger": "/apidocs"}), 200


@app.route("/api/v2/books", methods=["GET"])
def get_books():
    return api_response(data=list(books_db.values()))


@app.route("/api/v2/books/<book_id>", methods=["GET"])
def get_book(book_id):
    book = books_db.get(book_id)
    if not book:
        return api_response(message="Book not found", status=404, error="NOT_FOUND")
    return api_response(data=book)


@app.route("/api/v2/books", methods=["POST"])
def create_book():
    data = request.get_json()
    if not data or not data.get("title") or not data.get("author"):
        return api_response(message="Invalid input", status=400, error="BAD_REQUEST")

    book_id = str(uuid.uuid4())
    book = {
        "id": book_id,
        "title": data["title"],
        "author": data["author"],
        "publishedYear": data.get("publishedYear"),
    }
    books_db[book_id] = book
    return api_response(data=book, message="Created", status=201)


@app.route("/api/v2/books/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = books_db.get(book_id)
    if not book:
        return api_response(message="Book not found", status=404, error="NOT_FOUND")

    data = request.get_json()
    if not data or not all(k in data for k in ["title", "author", "publishedYear"]):
        return api_response(message="Invalid input", status=400, error="BAD_REQUEST")

    book.update({"title": data["title"], "author": data["author"], "publishedYear": data["publishedYear"]})
    return api_response(data=book, message="Updated")


@app.route("/api/v2/books/<book_id>", methods=["PATCH"])
def patch_book(book_id):
    book = books_db.get(book_id)
    if not book:
        return api_response(message="Book not found", status=404, error="NOT_FOUND")

    data = request.get_json()
    if not data:
        return api_response(message="Invalid input", status=400, error="BAD_REQUEST")

    for field in ["title", "author", "publishedYear"]:
        if field in data:
            book[field] = data[field]
    return api_response(data=book, message="Updated")


@app.route("/api/v2/books/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = books_db.pop(book_id, None)
    if not book:
        return api_response(message="Book not found", status=404, error="NOT_FOUND")
    return api_response(data=book, message="Deleted")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)

app = app