import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.product_create import ProductCreate  # noqa: E501
from openapi_server.models.product_list_response import ProductListResponse  # noqa: E501
from openapi_server.models.product_patch import ProductPatch  # noqa: E501
from openapi_server.models.product_response import ProductResponse  # noqa: E501
from openapi_server.models.stock_response import StockResponse  # noqa: E501
from openapi_server.models.stock_update import StockUpdate  # noqa: E501
from openapi_server import util
from .db import get_db

def format_mongo_doc(doc):
    """
    Chuyển đổi document của MongoDB để khớp với Response Model của Swagger.
    Đổi '_id' (ObjectId) thành 'id' (string).
    """
    if not doc:
        return None
    if '_id' in doc:
        doc['id'] = str(doc.pop('_id'))
    return doc

def safe_object_id(pid):
    """
    Thử parse ID sang dạng ObjectId của MongoDB.
    Nếu input đang là integer hoặc string thường, giữ nguyên để tránh lỗi crash.
    """
    try:
        return ObjectId(pid)
    except InvalidId:
        return pid

def create_product(body):  # noqa: E501
    """Tạo sản phẩm mới
     # noqa: E501
    :param product_create: 
    :type product_create: dict | bytes
    :rtype: Union[ProductResponse, Tuple[ProductResponse, int], Tuple[ProductResponse, int, Dict[str, str]]
    """
    product_create = body
    if connexion.request.is_json:
        product_create = ProductCreate.from_dict(connexion.request.get_json())  # noqa: E501

    db = get_db()
    # Map dữ liệu thành Dictionary để chèn vào MongoDB
    product_data = {
        "name": product_create.name,
        "description": product_create.description,
        "price": product_create.price,
        "sku": product_create.sku,
        "category_id": product_create.category_id,
        "stock_quantity": product_create.stock_quantity if product_create.stock_quantity is not None else 0,
        "status": product_create.status if product_create.status is not None else 'draft'
    }
    # Insert vào collection 'products'
    result = db.products.insert_one(product_data)
    # Gán _id vừa tạo vào object
    product_data['_id'] = result.inserted_id
    return {"data": format_mongo_doc(product_data)}, 201
#    return 'do some magic!'


def delete_product(product_id):  # noqa: E501
    """Xóa sản phẩm
     # noqa: E501
    :param product_id: ID của sản phẩm
    :type product_id: int
    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """

    db = get_db()
    # Xóa trực tiếp và kiểm tra số lượng bản ghi bị ảnh hưởng
    result = db.products.delete_one({"_id": safe_object_id(product_id)})
    if result.deleted_count == 0:
        return {"code": "NOT_FOUND", "message": "Không tìm thấy sản phẩm"}, 404
    return '', 204
#    return 'do some magic!'


def get_product(product_id):  # noqa: E501
    """Lấy chi tiết sản phẩm
     # noqa: E501
    :param product_id: ID của sản phẩm
    :type product_id: int
    :rtype: Union[ProductResponse, Tuple[ProductResponse, int], Tuple[ProductResponse, int, Dict[str, str]]
    """

    db = get_db()
    product = db.products.find_one({"_id": safe_object_id(product_id)})
    if product is None:
        return {"code": "NOT_FOUND", "message": "Không tìm thấy sản phẩm"}, 404
    return {"data": format_mongo_doc(product)}, 200
#    return 'do some magic!'


def list_products(category_id=None):  # noqa: E501
    """Lấy danh sách sản phẩm
     # noqa: E501
    :param category_id: Lọc theo danh mục
    :type category_id: int
    :rtype: Union[ProductListResponse, Tuple[ProductListResponse, int], Tuple[ProductListResponse, int, Dict[str, str]]
    """
    db = get_db()
    query = {}
    # Build query động nếu có filter
    if category_id is not None:
        query["category_id"] = category_id
    cursor = db.products.find(query)
    products = [format_mongo_doc(doc) for doc in cursor]
    return {"data": products}, 200
#    return 'do some magic!'


def patch_product(product_id, body):  # noqa: E501
    """Cập nhật một phần thông tin sản phẩm
     # noqa: E501
    :param product_id: ID của sản phẩm
    :type product_id: int
    :param product_patch: 
    :type product_patch: dict | bytes
    :rtype: Union[ProductResponse, Tuple[ProductResponse, int], Tuple[ProductResponse, int, Dict[str, str]]
    """
    product_patch = body
    if connexion.request.is_json:
        product_patch = ProductPatch.from_dict(connexion.request.get_json())  # noqa: E501
    db = get_db()

    # Lấy ra Dictionary loại bỏ những trường None
    patch_data = {k: v for k, v in product_patch.to_dict().items() if v is not None}
    if not patch_data:
        # Nếu không có gì để update, trả về object hiện tại
        product = db.products.find_one({"_id": safe_object_id(product_id)})
        if not product:
            return {"code": "NOT_FOUND", "message": "Không tìm thấy sản phẩm"}, 404
        return {"data": format_mongo_doc(product)}, 200
    # find_one_and_update với ReturnDocument.AFTER sẽ trả về record sau khi đã update xong (nguyên tử hóa)
    updated_product = db.products.find_one_and_update(
        {"_id": safe_object_id(product_id)},
        {"$set": patch_data},
        return_document=ReturnDocument.AFTER
    )

    if not updated_product:
        return {"code": "NOT_FOUND", "message": "Không tìm thấy sản phẩm"}, 404
    return {"data": format_mongo_doc(updated_product)}, 200
#    return 'do some magic!'


def update_product(product_id, body):  # noqa: E501
    """Cập nhật toàn bộ thông tin sản phẩm
     # noqa: E501
    :param product_id: ID của sản phẩm
    :type product_id: int
    :param product_create: 
    :type product_create: dict | bytes
    :rtype: Union[ProductResponse, Tuple[ProductResponse, int], Tuple[ProductResponse, int, Dict[str, str]]
    """
    product_create = body
    if connexion.request.is_json:
        product_create = ProductCreate.from_dict(connexion.request.get_json())  # noqa: E501
    db = get_db()
    # Object update toàn bộ
    update_data = {
        "name": product_create.name,
        "description": product_create.description,
        "price": product_create.price,
        "sku": product_create.sku,
        "category_id": product_create.category_id,
        "stock_quantity": product_create.stock_quantity if product_create.stock_quantity is not None else 0,
        "status": product_create.status if product_create.status is not None else 'draft'
    }

    updated_product = db.products.find_one_and_update(
        {"_id": safe_object_id(product_id)},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER
    )
    if not updated_product:
        return {"code": "NOT_FOUND", "message": "Không tìm thấy sản phẩm"}, 404
    return {"data": format_mongo_doc(updated_product)}, 200 
#    return 'do some magic!'


def update_stock(product_id, body):  # noqa: E501
    """Cập nhật tồn kho sản phẩm
     # noqa: E501
    :param product_id: ID của sản phẩm
    :type product_id: int
    :param stock_update: 
    :type stock_update: dict | bytes
    :rtype: Union[StockResponse, Tuple[StockResponse, int], Tuple[StockResponse, int, Dict[str, str]]
    """
    stock_update = body
    if connexion.request.is_json:
        stock_update = StockUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'