import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.category import Category  # noqa: E501
from openapi_server.models.category_create import CategoryCreate  # noqa: E501
from openapi_server.models.list_categories200_response import ListCategories200Response  # noqa: E501
from openapi_server import util


def create_category(body):  # noqa: E501
    """Tạo danh mục mới

     # noqa: E501

    :param category_create: 
    :type category_create: dict | bytes

    :rtype: Union[Category, Tuple[Category, int], Tuple[Category, int, Dict[str, str]]
    """
    category_create = body
    if connexion.request.is_json:
        category_create = CategoryCreate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def list_categories():  # noqa: E501
    """Lấy danh sách danh mục

     # noqa: E501


    :rtype: Union[ListCategories200Response, Tuple[ListCategories200Response, int], Tuple[ListCategories200Response, int, Dict[str, str]]
    """
    return 'do some magic!'
