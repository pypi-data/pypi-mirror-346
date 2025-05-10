from pydantic import BaseModel
from typing import Any


class BaseContent(BaseModel):
    options: dict[str, Any] = {}
