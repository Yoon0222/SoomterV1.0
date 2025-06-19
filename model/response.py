from pydantic import BaseModel
from typing import Any, Optional, Union

class APIResponse(BaseModel):
    success : bool
    code : Union[int, str]
    error : Optional[Any] = None
    data : Optional[Any] = None
    message : Optional[Any] = None
