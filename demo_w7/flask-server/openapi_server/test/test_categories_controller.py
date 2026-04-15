import unittest

from flask import json

from openapi_server.models.category import Category  # noqa: E501
from openapi_server.models.category_create import CategoryCreate  # noqa: E501
from openapi_server.models.list_categories200_response import ListCategories200Response  # noqa: E501
from openapi_server.test import BaseTestCase


class TestCategoriesController(BaseTestCase):
    """CategoriesController integration test stubs"""

    def test_create_category(self):
        """Test case for create_category

        Tạo danh mục mới
        """
        category_create = {"parent_id":0,"name":"Thời trang nam"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/categories',
            method='POST',
            headers=headers,
            data=json.dumps(category_create),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_categories(self):
        """Test case for list_categories

        Lấy danh sách danh mục
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/categories',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
