from flask_paginate import get_page_args, Pagination
from app.config_dashboard import per_page_number


def my_get_page_args(per_page=per_page_number):
    """Control the number of documents displayed per page"""

    page = get_page_args(page_parameter="page", per_page_parameter="per_page")[0]
    offset = (page - 1) * per_page

    return page, per_page, offset


# Pagination
def get_users_pagination(data_list, offset=0, per_page=10):
    """Return a interval of documents according to the page number"""
    return data_list[offset : offset + per_page]


def process_pagination(documents_processed):
    """Get the documents processed previously  and return the instance Pagination"""

    page, per_page, offset = my_get_page_args()

    if documents_processed:
        pagination_data = get_users_pagination(
            data_list=documents_processed["data_list"],
            offset=offset,
            per_page=per_page,
        )
        pagination = Pagination(
            page=page,  # request.values.get("page") if request.values.get("page") else 1 , # First page doesn't has ?page=1
            per_page=per_page,
            total=documents_processed["total_found"],
            css_framework="boostrap4",
        )
        return pagination_data, pagination

    return None
