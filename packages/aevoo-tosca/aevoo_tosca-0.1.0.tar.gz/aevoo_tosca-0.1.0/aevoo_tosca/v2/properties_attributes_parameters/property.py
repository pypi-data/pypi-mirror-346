from __future__ import annotations

from typing import Any

from pydantic import Field

from .attribute import AttributeAssignment
from .constraint_clause import ConstraintClause
from .schema import SchemaDefinition
from ..common.default_base_model import DefaultBaseModel

PropertyAssignment = AttributeAssignment


class PropertyDefinition(DefaultBaseModel):
    constraints: list[ConstraintClause] | None = None
    default: Any | None = None  # Must match property type
    description: str | None = None
    entry_schema: SchemaDefinition | None = None
    key_schema: SchemaDefinition | None = None
    metadata: dict[str, str] | None = None
    read_only: bool | None = False
    required: bool = True
    status: str = Field(default="supported")
    type: str
    # value: Any | None = None
    # external_schema: Optional[str]
