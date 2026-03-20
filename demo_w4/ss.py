import yaml
import jwt
import datetime
from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Book Management API V2',
    'uiversion': 3,
    'openapi': '3.0.0'
}

# Secret key để sign/verify JWT
JWT_SECRET = "super-secret-key-demo"
JWT_ALGORITHM = "HS256"

template_str = """
openapi: 3.0.0
info:
  title: Book API V2
  version: 2.0.0
  description: |
    API quản lý sách
servers:
  - url: http://localhost:5000
    description: Local dev server
tags:
  - name: Auth
    description: Xác thực - lấy JWT token
  - name: Books
    description: API quản lý sách Swagger
paths:
  /api/v2/auth/token:
    post:
      tags:
        - Auth
      summary: Đăng nhập - lấy JWT Bearer Token
      description: |
        Trả về JWT token. Dùng thông tin demo:
        - username: `admin`, password: `1234`  → role: admin
        - username: `user1`, password: `1234`  → role: user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/LoginInput"
      responses:
        "200":
          description: Đăng nhập thành công
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/TokenResponse"
        "401":
          description: Sai thông tin đăng nhập
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /api/v2/books/me:
    get:
      tags:
        - Books
      summary: Lấy sách của tôi (Demo JWT Bearer)
      description: |
        Endpoint yêu cầu JWT hợp lệ. Server decode token để lấy thông tin user.
        Chỉ trả về sách phù hợp với role của user trong token.
      security:
        - BearerAuth: []
      responses:
        "200":
          description: Thành công - trả về sách theo role
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/BookListResponse"
        "401":
          description: Token thiếu hoặc không hợp lệ
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
  /api/v2/books:
    get:
      tags:
        - Books
      summary: Lấy danh sách sách (Demo Query)
      parameters:
        - name: author
          in: query
          description: Lọc danh sách theo tên tác giả (VD nhập 'Thach Lam')
          required: false
          schema:
            type: string
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
                $ref: "#/components/schemas/ErrorResponse"
  /api/v2/books/{book_id}:
    get:
      tags:
        - Books
      summary: Lấy chi tiết sách
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
                $ref: "#/components/schemas/ErrorResponse"
    put:
      tags:
        - Books
      summary: Cập nhật sách
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
                $ref: "#/components/schemas/ErrorResponse"
    delete:
      tags:
        - Books
      summary: Xóa sách
      parameters:
        - $ref: "#/components/parameters/BookId"
        - name: X-API-Key
          in: header
          description: API Key để xác thực quyền xóa (nhập '12345')
          required: true
          schema:
            type: string
      responses:
        "200":
          description: Xóa thành công
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/BookResponse"
        "401":
          description: Không có quyền (Sai API Key)
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
        "404":
          description: Không tìm thấy
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        Nhập token theo định dạng: Bearer <token>
        Lấy token từ endpoint POST /api/v2/auth/token
  schemas:
    LoginInput:
      type: object
      required:
        - username
        - password
      properties:
        username:
          type: string
          example: admin
        password:
          type: string
          example: "1234"
    TokenResponse:
      type: object
      properties:
        status:
          type: integer
          example: 200
        message:
          type: string
          example: Login successful
        data:
          type: object
          properties:
            token:
              type: string
              example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
            expires_in:
              type: string
              example: 30 minutes
            payload:
              type: object
              description: Nội dung được encode trong token (để demo)
              properties:
                username:
                  type: string
                role:
                  type: string
                exp:
                  type: string
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
        owner:
          type: string
          example: admin
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
    ErrorResponse:
      type: object
      properties:
        status:
          type: integer
        message:
          type: string
        data:
          nullable: true
        error:
          type: string
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

DEMO_USERS = {
    "admin": {"password": "1234", "role": "admin"},
    "user1": {"password": "1234", "role": "user"},
}

books = [
    {"id": 1, "title": "Ho Quy Ly",          "author": "Nguyen Xuan Khanh", "publishedYear": 2000, "owner": "admin"},
    {"id": 2, "title": "Thuong nho muoi hai", "author": "Vu Bang",           "publishedYear": 1960, "owner": "user1"},
    {"id": 3, "title": "Gio dau mua",         "author": "Thach Lam",         "publishedYear": 1937, "owner": "admin"},
]
current_id = 4


# ── Helpers ───────────────────────────────────────────────────────────────────

def api_response(data=None, message="Success", status=200, error=None):
    return jsonify({
        "status": status,
        "message": message,
        "data": data,
        "error": error,
    }), status


def decode_bearer_token():
    """
    Đọc Authorization header, verify JWT, trả về payload.
    Raise ValueError nếu token thiếu hoặc không hợp lệ.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise ValueError("Missing or malformed Authorization header. Expected: Bearer <token>")

    token = auth_header.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token đã hết hạn. Vui lòng đăng nhập lại.")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Token không hợp lệ: {str(e)}")


# ── Auth endpoint ─────────────────────────────────────────────────────────────

@app.route('/api/v2/auth/token', methods=['POST'])
def login():
    """POST /api/v2/auth/token — trả về JWT nếu đúng thông tin."""
    data = request.get_json()
    if not data:
        return api_response(message="Invalid input", status=400, error="BAD_REQUEST")

    username = data.get("username", "")
    password = data.get("password", "")
    user = DEMO_USERS.get(username)

    if not user or user["password"] != password:
        return api_response(
            message="Sai username hoặc password",
            status=401,
            error="UNAUTHORIZED"
        )

    exp_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    payload = {
        "username": username,
        "role": user["role"],
        "exp": exp_time,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return api_response(
        data={
            "token": token,
            "expires_in": "30 minutes",
            "payload": {
                "username": username,
                "role": user["role"],
                "exp": exp_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
            }
        },
        message="Login successful",
        status=200
    )


# ── Book endpoints ────────────────────────────────────────────────────────────

@app.route('/api/v2/books/me', methods=['GET'])
def get_my_books():
    """
    GET /api/v2/books/me — Demo JWT Bearer Security Scheme.
    - admin : thấy tất cả sách
    - user  : chỉ thấy sách của chính mình (theo trường owner)
    """
    try:
        payload = decode_bearer_token()
    except ValueError as e:
        return api_response(message=str(e), status=401, error="UNAUTHORIZED")

    username = payload.get("username")
    role = payload.get("role")

    if role == "admin":
        result = books
        message = f"Xin chào {username} (role: admin) — trả về toàn bộ {len(result)} cuốn sách"
    else:
        result = [b for b in books if b.get("owner") == username]
        message = f"Xin chào {username} (role: user) — trả về {len(result)} cuốn sách của bạn"

    return api_response(data=result, message=message)


@app.route('/api/v2/books', methods=['GET'])
def get_books():
    """GET /api/v2/books — Demo Query Param."""
    author_query = request.args.get('author')
    if author_query:
        filtered = [b for b in books if author_query.lower() in b["author"].lower()]
        return api_response(data=filtered, message=f"Filtered by author: {author_query}")
    return api_response(data=books)


@app.route('/api/v2/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """GET /api/v2/books/<id> — Demo Path Param."""
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return api_response(data=book)
    return api_response(message="Book not found", status=404, error="NOT_FOUND")


@app.route('/api/v2/books', methods=['POST'])
def create_book():
    """POST /api/v2/books — Demo Cookie."""
    global current_id
    data = request.get_json()
    session_id = request.cookies.get('session_id')

    if not data or not data.get("title") or not data.get("author"):
        return api_response(message="Invalid input", status=400, error="BAD_REQUEST")

    new_book = {
        "id": current_id,
        "title": data["title"],
        "author": data["author"],
        "publishedYear": data.get("publishedYear"),
        "owner": "unknown",
    }
    books.append(new_book)
    current_id += 1

    message = "Created"
    if session_id:
        message += f" (Nhận được cookie session_id: {session_id})"
    return api_response(data=new_book, message=message, status=201)


@app.route('/api/v2/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """PUT /api/v2/books/<id>."""
    data = request.get_json()
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        book.update({
            "title": data.get("title", book["title"]),
            "author": data.get("author", book["author"]),
            "publishedYear": data.get("publishedYear", book["publishedYear"]),
        })
        return api_response(data=book, message="Updated")
    return api_response(message="Book not found", status=404, error="NOT_FOUND")


@app.route('/api/v2/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """DELETE /api/v2/books/<id> — Demo Header Param (X-API-Key)."""
    global books
    api_key = request.headers.get('X-API-Key')
    if api_key != '12345':
        return api_response(
            message="Unauthorized. Sai hoặc thiếu X-API-Key.",
            status=401,
            error="UNAUTHORIZED"
        )
    initial_len = len(books)
    books = [b for b in books if b["id"] != book_id]
    if len(books) < initial_len:
        return api_response(message="Deleted", status=200)
    return api_response(message="Book not found", status=404, error="NOT_FOUND")


if __name__ == '__main__':
    app.run(debug=True, port=5000)