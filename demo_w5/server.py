import json
from flask import Flask, request, jsonify

app = Flask(__name__)

with open('MOCK_DATA.json', 'r', encoding='utf-8') as f:
    all_data = json.load(f)

@app.route('/api/items', methods=['GET'])
def get_items():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    start_index = (page - 1) * limit
    end_index = start_index + limit

    paginated_data = all_data[start_index:end_index]

    return jsonify({
        "page": page,
        "limit": limit,
        "total_items": len(all_data),
        "total_pages": (len(all_data) + limit - 1) // limit, 
        "data": paginated_data
    })

@app.route('/api/items-cursor', methods=['GET'])
def get_items_cursor():
    cursor = request.args.get('cursor', default=0, type=int)
    limit = request.args.get('limit', default=10, type=int)

    items_after_cursor = [item for item in all_data if item['id'] > cursor]

    result_data = items_after_cursor[:limit]

    next_cursor = None
    if len(result_data) > 0:
        next_cursor = result_data[-1]['id']

    has_more = len(items_after_cursor) > limit

    return jsonify({
        "data": result_data,
        "next_cursor": next_cursor,
        "has_more": has_more
    })

@app.route('/api/items/offset', methods=['GET'])
def get_items_offset():
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', default=10, type=int)

    result_data = all_data[offset : offset + limit]

    next_offset = offset + limit
    has_more = next_offset < len(all_data)

    return jsonify({
        "data": result_data,
        "meta": {
            "offset_hien_tai": offset,
            "limit": limit,
            "tong_so_item": len(all_data),
            "next_offset": next_offset if has_more else None
        }
    })

@app.route('/api/items-keyset', methods=['GET'])
def get_items_keyset():
    limit = request.args.get('limit', default=10, type=int)
    last_id = request.args.get('last_id', default=0, type=int)

    filtered_data = [item for item in all_data_sorted if item['id'] > last_id]

    result_data = filtered_data[:limit]

    next_last_id = None
    if len(result_data) > 0:
        next_last_id = result_data[-1]['id']

    has_more = len(filtered_data) > limit

    return jsonify({
        "data": result_data,
        "meta": {
            "limit": limit,
            "next_last_id": next_last_id if has_more else None,
            "has_more": has_more
        }
    })

all_data_sorted = sorted(all_data, key=lambda x: x['created_at'], reverse=True)

@app.route('/api/items-time', methods=['GET'])
def get_items_time():
    limit = request.args.get('limit', default=10, type=int)
    last_created_at = request.args.get('last_created_at', default=None, type=str)

    if last_created_at:
        filtered_data = [item for item in all_data_sorted if item['created_at'] < last_created_at]
    else:
        filtered_data = all_data_sorted

    result_data = filtered_data[:limit]

    next_last_created_at = None
    if len(result_data) > 0:
        next_last_created_at = result_data[-1]['created_at']

    has_more = len(filtered_data) > limit

    return jsonify({
        "data": result_data,
        "meta": {
            "limit": limit,
            "next_last_created_at": next_last_created_at if has_more else None,
            "has_more": has_more
        }
    })
if __name__ == '__main__':
    app.run(debug=True)