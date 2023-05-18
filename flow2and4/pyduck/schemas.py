"""
This is the module for defining schemas related pyduck.
"""

from pydantic import BaseModel, ValidationError, conint, validator


class PyduckSchema(BaseModel):
    """Represent base schema."""

    class Config:
        orm_mode = True
        # whether to allow arbitrary user types for fields (they are validated
        # simply by checking if the value is an instance of the type). If `False`,
        # `RuntimeError` will be raised on model declaration.
        arbitrary_types_allowed = True
        # whether to strip leading and trailing whitespace for str * byte types
        anystr_strip_whitespace = True


class CommonParameters(BaseModel):
    """Represent common parameters used for search, query, pagination globally.

    
    :filters
        multiple filters are delimited by single whitspace(' ') which can be
        splited by `filters.split()`

        each filter __MUST__ have follow the form `<field>-<op>-<value>` form
        `<field>` is the database column(or property) and `<op>` is operator 
        and `<value>` is the value used to filter `<field>`.
    

    [stolen and modified from]
    https://github.com/Netflix/dispatch/blob/master/src/dispatch/database/service.py#L427
    """

    page: conint(gt=0, lt=2147483647) = 1
    per_page: conint(gt=0, le=50) = 10
    max_per_page: conint(gt=0, le=100) = 100
    filters: str | None
    sorters: str | None
    periods: str | None
    query: str | None
