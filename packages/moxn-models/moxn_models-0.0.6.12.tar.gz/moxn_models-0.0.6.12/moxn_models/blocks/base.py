from typing import Any

from pydantic import BaseModel


class BaseContent(BaseModel):
    options: dict[str, Any] = {}
