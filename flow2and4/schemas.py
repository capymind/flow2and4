"""
This is the module for defining schemas.
"""

from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Represent base schema."""

    class Config:
        orm_mode = True
        # whether to allow arbitrary user types for fields (they are validated
        # simply by checking if the value is an instance of the type). If `False`,
        # `RuntimeError` will be raised on model declaration.
        arbitrary_types_allowed = True
        # whether to strip leading and trailing whitespace for str * byte types
        anystr_strip_whitespace = True
