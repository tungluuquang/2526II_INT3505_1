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

    
    conn = get_db()
    cur = conn.cursor()
    
    # Rút dữ liệu từ Object do tool gen ra (có thể dùng .property hoặc get dict)
    cur.execute('''
        INSERT INTO products (name, description, price, sku, category_id, stock_quantity, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        product_create.name,
        product_create.description,
        product_create.price,
        product_create.sku,
        product_create.category_id,
        product_create.stock_quantity if product_create.stock_quantity is not None else 0,
        product_create.status if product_create.status is not None else 'draft'
    ))
    
    conn.commit()
    new_id = cur.lastrowid # ID tự tăng vừa được tạo
    
    cur.execute("SELECT * FROM products WHERE id = ?", (new_id,))
    new_product = cur.fetchone()
    conn.close()
    
    return {"data": dict(new_product)}, 201
#    return 'do some magic!'


def delete_product(product_id):  # noqa: E501
    """Xóa sản phẩm

     # noqa: E501

    :param product_id: ID của sản phẩm
    :type product_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """

    conn = get_db()
    
    if conn.execute("SELECT id FROM products WHERE id = ?", (product_id,)).fetchone() is None:
        conn.close()
        return {"code": "NOT_FOUND", "message": "Không tìm thấy sản phẩm"}, 404
        
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    
    return '', 204
#    return 'do some magic!'


def get_product(product_id):  # noqa: E501
    """Lấy chi tiết sản phẩm

     # noqa: E501

    :param product_id: ID của sản phẩm
    :type product_id: int

    :rtype: Union[ProductResponse, Tuple[ProductResponse, int], Tuple[ProductResponse, int, Dict[str, str]]
    """

    conn = get_db()
    cur = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cur.fetchone()
    conn.close()
    
    if product is None:
        return {"code": "NOT_FOUND", "message": "Không tìm thấy sản phẩm"}, 404
        
    return {"data": dict(product)}, 200
#    return 'do some magic!'


def list_products(category_id=None):  # noqa: E501
    """Lấy danh sách sản phẩm

     # noqa: E501

    :param category_id: Lọc theo danh mục
    :type category_id: int

    :rtype: Union[ProductListResponse, Tuple[ProductListResponse, int], Tuple[ProductListResponse, int, Dict[str, str]]
    """
        conn = get_db()
    
    if category_id is not None:
        cur = conn.execute("SELECT * FROM products WHERE category_id = ?", (category_id,))
    else:
        cur = conn.execute("SELECT * FROM products")
        
    products = [dict(row) for row in cur.fetchall()]
    conn.close()
    
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
        
    conn = get_db()
    if conn.execute("SELECT id FROM products WHERE id = ?", (product_id,)).fetchone() is None:
        conn.close()
        return {"code": "NOT_FOUND", "message": "Không tìm thấy sản phẩm"}, 404

    # Lấy ra dạng Dictionary để loại bỏ những trường bị None (người dùng không gửi lên)
    patch_data = {k: v for k, v in product_patch.to_dict().items() if v is not None}
    
    if patch_data:
        # Tự động gen câu lệnh UPDATE dựa trên những key được gửi lên
        set_clause = ", ".join([f"{key} = ?" for key in patch_data.keys()])
        values = list(patch_data.values())
        values.append(product_id) # ID cho mệnh đề WHERE
        
        conn.execute(f"UPDATE products SET {set_clause} WHERE id = ?", tuple(values))
        conn.commit()

    cur = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    updated_product = cur.fetchone()
    conn.close()
    
    return {"data": dict(updated_product)}, 200
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

    conn = get_db()
    if conn.execute("SELECT id FROM products WHERE id = ?", (product_id,)).fetchone() is None:
        conn.close()
        return {"code": "NOT_FOUND", "message": "Không tìm thấy sản phẩm"}, 404

    conn.execute('''
        UPDATE products 
        SET name=?, description=?, price=?, sku=?, category_id=?, stock_quantity=?, status=?
        WHERE id = ?
    ''', (
        product_create.name,
        product_create.description,
        product_create.price,
        product_create.sku,
        product_create.category_id,
        product_create.stock_quantity if product_create.stock_quantity is not None else 0,
        product_create.status if product_create.status is not None else 'draft',
        product_id
    ))
    
    conn.commit()
    cur = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    updated_product = cur.fetchone()
    conn.close()
    
    return {"data": dict(updated_product)}, 200    
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
