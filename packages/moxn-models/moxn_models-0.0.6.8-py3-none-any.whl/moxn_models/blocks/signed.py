from moxn_models.blocks.base import BaseContent
from datetime import datetime


class SignedURLContent(BaseContent):
    key: str
    expiration: datetime | None = None
    ttl_seconds: int = 3600
    buffer_seconds: int = 300
    signed_url: str | None = None
