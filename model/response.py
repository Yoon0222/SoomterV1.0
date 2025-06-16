from pydantic import BaseModel
from typing import Any, Optional

class APIResponse(BaseModel):
    success : bool
    code : str
    error : Optional[Any] = None
    data : Optional[Any] = None
    message : Optional[Any] = None
