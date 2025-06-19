from model.response import APIResponse
from typing import Any, Optional, Union, List, Type
from pydantic import BaseModel

from model.code import success
def make_response(
        data=None,
        code=success,
        error=None,
        message=None,
        schema_class: Optional[Type[BaseModel]] = None
) -> APIResponse:

    # SQLAlchemy → Pydantic 변환 처리
    if schema_class and isinstance(data, list):
        data = [schema_class.from_orm(item) for item in data]

    elif schema_class and isinstance(data, object):
        data = schema_class.from_orm(data)

    return APIResponse(
        success = error is None,
        data = data,
        code = code,
        error = error,
        message = message
    )