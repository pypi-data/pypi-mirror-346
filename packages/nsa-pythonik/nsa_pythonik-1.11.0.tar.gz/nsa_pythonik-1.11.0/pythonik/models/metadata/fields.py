# pythonik/models/metadata/fields.py
from typing import List, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, HttpUrl

class IconikFieldType(str, Enum):
    """Known Iconik metadata field types based on documentation.
    Actual values sent to/received from API.
    """
    STRING = "string"        # General short text
    TEXT = "text"            # Longer text (potentially multi-line in UI but distinct type)
    TEXT_AREA = "text_area"  # Explicitly for larger amounts of text data
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"      # For Yes/No fields
    DATE = "date"
    DATETIME = "datetime"    # For Date Time fields
    DROPDOWN = "drop_down"   # For fields with predefined options
    EMAIL = "email"
    TAG_CLOUD = "tag_cloud"  # For free-form tag collections
    URL = "url"

class FieldOption(BaseModel):
    """Represents an option for a metadata field (e.g., for dropdowns)."""
    label: Optional[str] = None
    value: Optional[str] = None

class _FieldConfigurable(BaseModel):
    """Base model for common configurable attributes of metadata fields."""
    label: Optional[str] = None
    field_type: Optional[IconikFieldType] = None
    description: Optional[str] = None
    options: Optional[List[FieldOption]] = None
    required: Optional[bool] = None
    auto_set: Optional[bool] = None
    hide_if_not_set: Optional[bool] = None
    is_block_field: Optional[bool] = None
    is_warning_field: Optional[bool] = None
    multi: Optional[bool] = None
    read_only: Optional[bool] = None
    representative: Optional[bool] = None
    sortable: Optional[bool] = None
    use_as_facet: Optional[bool] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    external_id: Optional[str] = None
    source_url: Optional[HttpUrl] = None

class FieldCreate(_FieldConfigurable):
    """Data Transfer Object for creating a new metadata field."""
    name: str
    label: str
    field_type: IconikFieldType

class FieldUpdate(_FieldConfigurable):
    """
    Data Transfer Object for updating an existing metadata field.
    All fields are optional to support partial updates.
    'name' is specified in the URL path for updates, not in the body.
    """
    pass

class Field(_FieldConfigurable):
    """Represents a metadata field as returned by the API."""
    id: str
    name: str
    label: str
    field_type: IconikFieldType

    date_created: Optional[datetime] = None
    date_modified: Optional[datetime] = None
    mapped_field_name: Optional[str] = None
