from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)

app.config['SWAGGER'] = {
    'title': 'Book Management API',
    'uiversion': 3,
    'openapi': '3.0.0'
}

template = {
    "openapi": "3.0.0",
    "info": {
        "title": "Book API",
        "version": "1.0.0",
        "description": "API quản lý sách đơn giản sử dụng Flask + Swagger"
    },
    "components": {
        "schemas": {

            "Book": {
                "type": "object",
                "required": ["id", "title", "author"],
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "title": {"type": "string", "example": "Hai dua tre"},
                    "author": {"type": "string", "example": "Thach Lam"},
                    "publishedYear": {"type": "integer", "example": 1938}
                },
                "example": {
                    "id": 1,
                    "title": "Hai dua tre",
                    "author": "Thach Lam",
                    "publishedYear": 1938
                }
            },

            "BookInput": {
                "type": "object",
                "required": ["title", "author"],
                "properties": {
                    "title": {
                        "type": "string",
                        "example": "Doraemon"
                    },
                    "author": {
                        "type": "string",
                        "example": "Fujiko F Fujio"
                    },
                    "publishedYear": {
                        "type": "integer",
                        "example": 1970
                    }
                }
            },

            "BookUpdate": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "example": "Updated title"
                    },
                    "author": {
                        "type": "string",
                        "example": "Updated author"
                    },
                    "publishedYear": {
                        "type": "integer",
                        "example": 2020
                    }
                }
            },

            "BookResponse": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "integer",
                        "example": 200
                    },
                    "message": {
                        "type": "string",
                        "example": "Success"
                    },
                    "data": {
                        "$ref": "#/components/schemas/Book"
                    },
                    "error": {
                        "type": "string",
                        "nullable": True,
                        "example": None
                    }
                }
            },

            "BookListResponse": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "integer",
                        "example": 200
                    },
                    "message": {
                        "type": "string",
                        "example": "Success"
                    },
                    "data": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/Book"
                        }
                    },
                    "error": {
                        "type": "string",
                        "nullable": True,
                        "example": None
                    }
                }
            }
        }
    }
}

swagger = Swagger(app, template=template)

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


# GET ALL BOOKS
@app.route('/api/v1/books', methods=['GET'])
def get_books():
    """
    Lấy danh sách tất cả sách
    ---
    tags:
      - Books
    responses:
      200:
        description: Thành công
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BookListResponse'
    """
    return api_response(data=books)


# GET ONE BOOK
@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Lấy thông tin chi tiết sách
    ---
    tags:
      - Books
    parameters:
      - name: book_id
        in: path
        schema:
          type: integer
        required: true
        description: ID sách
    responses:
      200:
        description: Thành công
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BookResponse'
      404:
        description: Không tìm thấy
    """
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return api_response(data=book)
    return api_response(message="Book not found", status=404, error="NOT_FOUND")


# CREATE BOOK
@app.route('/api/v1/books', methods=['POST'])
def create_book():
    """
    Thêm sách mới
    ---
    tags:
      - Books
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/BookInput'
    responses:
      201:
        description: Tạo thành công
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BookResponse'
      400:
        description: Lỗi dữ liệu
    """
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


# UPDATE BOOK
@app.route('/api/v1/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Cập nhật sách
    ---
    tags:
      - Books
    parameters:
      - name: book_id
        in: path
        schema:
          type: integer
        required: true
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/BookUpdate'
    responses:
      200:
        description: Thành công
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BookResponse'
      404:
        description: Không tìm thấy
    """
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


# DELETE BOOK 
@app.route('/api/v1/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Xóa sách
    ---
    tags:
      - Books
    parameters:
      - name: book_id
        in: path
        schema:
          type: integer
        required: true
    responses:
      200:
        description: Xóa thành công
      404:
        description: Không tìm thấy
    """
    global books
    initial_length = len(books)
    books = [b for b in books if b["id"] != book_id]

    if len(books) < initial_length:
        return api_response(message="Deleted", status=200)

    return api_response(message="Book not found", status=404, error="NOT_FOUND")


if __name__ == '__main__':
    app.run(debug=True, port=5000) 