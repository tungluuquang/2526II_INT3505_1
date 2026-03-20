import yaml
from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__, static_folder=None, template_folder=None)

app.config['SWAGGER'] = {
    'title': 'Book Management API V2',
    'uiversion': 3,
    'openapi': '3.0.0'
}

# servers:
#   - url: http://localhost:5000
#     description: Local dev server
template_str = """
openapi: 3.0.0
info:
  title: Book API V2
  version: 2.0.0
  description: API quản lý sách

servers:
  - url: http://2526-ii-int-3505-1-41v9d2qr8-tungluuquangs-projects.vercel.app
    description: Production Server (Vercel)
  - url: http://localhost:5000
    description: Local Development Server

tags:
  - name: Books
    description: API quản lý sách Swagger

paths:
  /api/v2/books:
    get:
      tags:
        - Books
      summary: Lấy danh sách sách
      operationId: getAllBooks
      parameters:
        - name: theme
          in: cookie
          required: false
          schema:
            type: string
            enum: [light, dark]
          description: UI theme
      responses:
        "200":
          description: Thành công
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/BookListResponse"

    post:
      tags:
        - Books
      summary: Tạo sách mới
      description: Tạo sách mới bằng tên, tác giả và năm sáng tác
      operationId: createBook
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/BookInput"
      responses:
        "201":
          description: Tạo thành công
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/BookResponse"
        "400":
          description: Dữ liệu không hợp lệ
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/BookResponse"

  /api/v2/books/{book_id}:
    get:
      tags:
        - Books
      summary: Lấy chi tiết sách
      operationId: getBookById
      parameters:
        - $ref: "#/components/parameters/BookId"
      responses:
        "200":
          description: Thành công
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/BookResponse"
        "404":
          description: Không tìm thấy
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/BookResponse"

    put:
      tags:
        - Books
      summary: Cập nhật sách
      operationId: updateBook
      parameters:
        - $ref: "#/components/parameters/BookId"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/BookUpdate"
      responses:
        "200":
          description: Cập nhật thành công
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/BookResponse"
        "404":
          description: Không tìm thấy
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/BookResponse"

    delete:
      tags:
        - Books
      summary: Xóa sách
      operationId: deleteBook
      parameters:
        - $ref: "#/components/parameters/BookId"
      responses:
        "200":
          description: Xóa thành công
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/BookResponse"
        "404":
          description: Không tìm thấy
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/BookResponse"

components:
  schemas:
    Book:
      type: object
      required:
        - id
        - title
        - author
      properties:
        id:
          type: integer
          example: 1
        title:
          type: string
          example: Hai dua tre
        author:
          type: string
          example: Thach Lam
        publishedYear:
          type: integer
          example: 1938

    BookInput:
      type: object
      required:
        - title
        - author
      properties:
        title:
          type: string
          example: Doraemon
        author:
          type: string
          example: Fujiko F Fujio
        publishedYear:
          type: integer
          example: 1970

    BookUpdate:
      type: object
      properties:
        title:
          type: string
        author:
          type: string
        publishedYear:
          type: integer

    BookResponse:
      type: object
      properties:
        status:
          type: integer
          example: 200
        message:
          type: string
          example: Success
        data:
          $ref: "#/components/schemas/Book"
        error:
          type: string
          nullable: true

    BookListResponse:
      type: object
      properties:
        status:
          type: integer
          example: 200
        message:
          type: string
          example: Success
        data:
          type: array
          items:
            $ref: "#/components/schemas/Book"
        error:
          type: string
          nullable: true

  parameters:
    BookId:
      name: book_id
      in: path
      required: true
      schema:
        type: integer
      description: ID của sách
"""

template = yaml.safe_load(template_str)

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
@app.route('/api/v2/books', methods=['GET'])
def get_books():
    return api_response(data=books)


# GET ONE BOOK
@app.route('/api/v2/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return api_response(data=book)
    return api_response(message="Book not found", status=404, error="NOT_FOUND")


# CREATE BOOK
@app.route('/api/v2/books', methods=['POST'])
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


# UPDATE BOOK
@app.route('/api/v2/books/<int:book_id>', methods=['PUT'])
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


# DELETE BOOK 
@app.route('/api/v2/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    initial_length = len(books)
    books = [b for b in books if b["id"] != book_id]

    if len(books) < initial_length:
        return api_response(message="Deleted", status=200)

    return api_response(message="Book not found", status=404, error="NOT_FOUND")

@app.route('/')
def home():
    return jsonify({"message": "API is running", "swagger": "/apidocs/"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

app = app