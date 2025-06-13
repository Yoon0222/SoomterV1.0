from pydantic import BaseModel
from typing import Any, Optional

class APIResponse(BaseModel):
    success : bool
    code : int
    error : Optional[Any] = None
    data : Optional[Any] = None
    message : Optional[Any] = None
