from enum import Enum
from typing import Literal
from moxn_models.blocks.base import BaseContent
from moxn_models.blocks.context import VariableType


# 1. Enums
# --------------------------------------------------------------------------- #
class VariableFormat(str, Enum):
    INLINE = "inline"
    BLOCK = "block"


# --------------------------------------------------------------------------- #
# 2. Base Variable class
# --------------------------------------------------------------------------- #
class VariableContentModel(BaseContent):
    """Base class for all variable types."""

    name: str
    variable_type: VariableType
    format: VariableFormat
    description: str = ""
    required: bool = True


class TextVariableModel(VariableContentModel):
    """A variable that represents text content."""

    variable_type: Literal[VariableType.PRIMITIVE] = VariableType.PRIMITIVE
    default_value: str | None = None


class ImageVariableModel(VariableContentModel):
    """A variable that represents image content."""

    variable_type: Literal[VariableType.IMAGE] = VariableType.IMAGE


class DocumentVariableModel(VariableContentModel):
    """A variable that represents document content (PDF)."""

    variable_type: Literal[VariableType.DOCUMENT] = VariableType.DOCUMENT
