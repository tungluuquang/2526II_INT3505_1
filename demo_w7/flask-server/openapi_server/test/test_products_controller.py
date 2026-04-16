import unittest

from flask import json

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.product_create import ProductCreate  # noqa: E501
from openapi_server.models.product_list_response import ProductListResponse  # noqa: E501
from openapi_server.models.product_patch import ProductPatch  # noqa: E501
from openapi_server.models.product_response import ProductResponse  # noqa: E501
from openapi_server.models.stock_response import StockResponse  # noqa: E501
from openapi_server.models.stock_update import StockUpdate  # noqa: E501
from openapi_server.test import BaseTestCase


class TestProductsController(BaseTestCase):
    """ProductsController integration test stubs"""

    def test_create_product(self):
        """Test case for create_product

        Tạo sản phẩm mới
        """
        product_create = {"price":199000,"name":"Áo Thun Nam Basic","description":"description","sku":"ATN-BASIC-001","stock_quantity":0,"status":"draft"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/products',
            method='POST',
            headers=headers,
            data=json.dumps(product_create),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_product(self):
        """Test case for delete_product

        Xóa sản phẩm
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/products/{product_id}'.format(product_id=1),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_product(self):
        """Test case for get_product

        Lấy chi tiết sản phẩm
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/products/{product_id}'.format(product_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_products(self):
        """Test case for list_products

        Lấy danh sách sản phẩm
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/products',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_patch_product(self):
        """Test case for patch_product

        Cập nhật một phần thông tin sản phẩm
        """
        product_patch = {"price":0.8008281904610115,"name":"name","description":"description","stock_quantity":6}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/products/{product_id}'.format(product_id=1),
            method='PATCH',
            headers=headers,
            data=json.dumps(product_patch),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_product(self):
        """Test case for update_product

        Cập nhật toàn bộ thông tin sản phẩm
        """
        product_create = {"price":199000,"name":"Áo Thun Nam Basic","description":"description","sku":"ATN-BASIC-001","stock_quantity":0,"status":"draft"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/products/{product_id}'.format(product_id=1),
            method='PUT',
            headers=headers,
            data=json.dumps(product_create),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_stock(self):
        """Test case for update_stock

        Cập nhật tồn kho sản phẩm
        """
        stock_update = {"quantity":20,"action":"set"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/products/{product_id}/stock'.format(product_id=1),
            method='PATCH',
            headers=headers,
            data=json.dumps(stock_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
