import connexion
from typing import Dict, Tuple, Union

from openapi_server.models.product_create import ProductCreate
from openapi_server.models.product_patch import ProductPatch
from openapi_server.models.stock_update import StockUpdate

from .db import get_db
from pymongo import ReturnDocument


def format_mongo_doc(doc):
    """Convert _id -> id"""
    if not doc:
        return None
    if "_id" in doc:
        doc["id"] = doc.pop("_id")  
    return doc


def get_next_sequence(db, name):
    """Auto increment id"""
    counter = db.counters.find_one_and_update(
        {"_id": name},
        {"$inc": {"seq": 1}},
        return_document=ReturnDocument.AFTER,
        upsert=True
    )
    return counter["seq"]


def validate_product_create(p):
    if p.name is None:
        return "Thiếu name"
    if p.price is None:
        return "Thiếu price"
    return None


def create_product(body):
    try:
        product_create = body
        if connexion.request.is_json:
            product_create = ProductCreate.from_dict(connexion.request.get_json())

        err = validate_product_create(product_create)
        if err:
            return {"code": "INVALID_INPUT", "message": err}, 400

        db = get_db()
        new_id = get_next_sequence(db, "product_id")

        product_data = {
            "_id": new_id,
            "name": product_create.name,
            "description": product_create.description,
            "price": product_create.price,
            "sku": product_create.sku,
            "stock_quantity": product_create.stock_quantity or 0,
            "status": product_create.status or "draft"
        }

        db.products.insert_one(product_data)

        return {"data": format_mongo_doc(product_data)}, 201

    except Exception as e:
        return {"code": "SERVER_ERROR", "message": str(e)}, 500


def get_product(product_id):
    try:
        db = get_db()
        product_id = int(product_id)

        product = db.products.find_one({"_id": product_id})
        if not product:
            return {"code": "NOT_FOUND", "message": "Không tìm thấy sản phẩm"}, 404

        return {"data": format_mongo_doc(product)}, 200

    except Exception as e:
        return {"code": "SERVER_ERROR", "message": str(e)}, 500


def list_products():
    try:
        db = get_db()
        products = [format_mongo_doc(doc) for doc in db.products.find()]
        return {"data": products}, 200

    except Exception as e:
        return {"code": "SERVER_ERROR", "message": str(e)}, 500


def delete_product(product_id):
    try:
        db = get_db()
        product_id = int(product_id)

        result = db.products.delete_one({"_id": product_id})
        if result.deleted_count == 0:
            return {"code": "NOT_FOUND", "message": "Không tìm thấy sản phẩm"}, 404

        return "", 204

    except Exception as e:
        return {"code": "SERVER_ERROR", "message": str(e)}, 500


def patch_product(product_id, body):
    try:
        product_patch = body
        if connexion.request.is_json:
            product_patch = ProductPatch.from_dict(connexion.request.get_json())

        db = get_db()
        product_id = int(product_id)

        patch_data = {
            k: v for k, v in product_patch.to_dict().items()
            if v is not None
        }

        if not patch_data:
            product = db.products.find_one({"_id": product_id})
            if not product:
                return {"code": "NOT_FOUND", "message": "Không tìm thấy sản phẩm"}, 404
            return {"data": format_mongo_doc(product)}, 200

        updated = db.products.find_one_and_update(
            {"_id": product_id},
            {"$set": patch_data},
            return_document=ReturnDocument.AFTER
        )

        if not updated:
            return {"code": "NOT_FOUND", "message": "Không tìm thấy sản phẩm"}, 404

        return {"data": format_mongo_doc(updated)}, 200

    except Exception as e:
        return {"code": "SERVER_ERROR", "message": str(e)}, 500


def update_product(product_id, body):
    try:
        product_create = body
        if connexion.request.is_json:
            product_create = ProductCreate.from_dict(connexion.request.get_json())

        db = get_db()
        product_id = int(product_id)

        update_data = {
            "name": product_create.name,
            "description": product_create.description,
            "price": product_create.price,
            "sku": product_create.sku,
            "stock_quantity": product_create.stock_quantity or 0,
            "status": product_create.status or "draft"
        }

        updated = db.products.find_one_and_update(
            {"_id": product_id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )

        if not updated:
            return {"code": "NOT_FOUND", "message": "Không tìm thấy sản phẩm"}, 404

        return {"data": format_mongo_doc(updated)}, 200

    except Exception as e:
        return {"code": "SERVER_ERROR", "message": str(e)}, 500


def update_stock(product_id, body):
    try:
        stock_update = body
        if connexion.request.is_json:
            stock_update = StockUpdate.from_dict(connexion.request.get_json())

        db = get_db()
        product_id = int(product_id)

        if stock_update.quantity is None:
            return {"code": "INVALID_INPUT", "message": "Thiếu quantity"}, 400

        updated = db.products.find_one_and_update(
            {"_id": product_id},
            {"$inc": {"stock_quantity": stock_update.quantity}},
            return_document=ReturnDocument.AFTER
        )

        if not updated:
            return {"code": "NOT_FOUND", "message": "Không tìm thấy sản phẩm"}, 404

        return {
            "data": {
                "product_id": updated["_id"],
                "stock_quantity": updated["stock_quantity"]
            }
        }, 200

    except Exception as e:
        return {"code": "SERVER_ERROR", "message": str(e)}, 500