from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock Database
authors_db = [
    {"id": 1, "name": "Nam Cao"},
    {"id": 2, "name": "To Hoai"}
]

books_db = [
    {"id": 101, "title": "Chi Pheo", "author_id": 1, "year": 1941, "category": "drama"},
    {"id": 102, "title": "Lao Hac", "author_id": 1, "year": 1943, "category": "drama"},
    {"id": 103, "title": "De Men Phieu Luu Ky", "author_id": 2, "year": 1941, "category": "adventure"},
    {"id": 104, "title": "Vo Nhat", "author_id": 3, "year": 1962, "category": "drama"}, 
]

reviews_db = [
    {"id": 1, "book_id": 101, "rating": 5, "comment": "Kinh dien!"},
    {"id": 2, "book_id": 103, "rating": 4, "comment": "Rat hay cho thieu nhi."}
]

# 1. NAMING CONVENTION

# SAI: @app.route('/getBooks', methods=['GET'])
# ĐÚNG:
@app.route('/books', methods=['GET'])
def get_books():
    """
    Kết hợp cả FILTERING, SORTING & PAGINATION vào resource danh sách gốc.
    URL Demo: /books?category=drama&sort=-year&page=1&limit=2
    """
    result = books_db.copy()

    # --- FILTERING ---
    category = request.args.get('category')
    year = request.args.get('year', type=int)
    
    if category:
        result = [b for b in result if b['category'] == category]
    if year:
        result = [b for b in result if b['year'] == year]

    # --- SORTING ---
    # sort_by: "year" (Tăng dần), "-year" (Giảm dần)
    sort_by = request.args.get('sort')
    if sort_by:
        descending = sort_by.startswith('-')
        sort_field = sort_by.lstrip('-')
        # Kiểm tra field có tồn tại không để tránh lỗi
        if len(result) > 0 and sort_field in result[0]:
            result.sort(key=lambda x: x[sort_field], reverse=descending)

    # --- PAGINATION ---
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_result = result[start_idx:end_idx]

    return jsonify({
        "total": len(result),
        "page": page,
        "limit": limit,
        "data": paginated_result
    }), 200


# 2. HIERARCHY & RELATIONSHIPS 
# Lấy danh sách sách của một tác giả cụ thể
# SAI: @app.route('/books/author/<int:author_id>', methods=['GET'])
# ĐÚNG:
@app.route('/authors/<int:author_id>/books', methods=['GET'])
def get_author_books(author_id):
    author_books = [b for b in books_db if b['author_id'] == author_id]
    return jsonify({"data": author_books}), 200


# 3. FLAT DESIGN / NESTING LIMITS 

# Yêu cầu: Lấy đánh giá (reviews) của cuốn sách "Chi Pheo" (id=101) do "Nam Cao" (id=1) viết.
# SAI: @app.route('/authors/<int:author_id>/books/<int:book_id>/reviews', methods=['GET']) -> QUÁ DÀI, LỒNG 3 CẤP
# ĐÚNG:
@app.route('/books/<int:book_id>/reviews', methods=['GET'])
def get_book_reviews(book_id):
    book_reviews = [r for r in reviews_db if r['book_id'] == book_id]
    return jsonify({"data": book_reviews}), 200

# Single Resource Access
@app.route('/books/<int:book_id>', methods=['GET'])
def get_single_book(book_id):
    book = next((b for b in books_db if b['id'] == book_id), None)
    if book:
        return jsonify({"data": book}), 200
    return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)