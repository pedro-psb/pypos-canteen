from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveFloat, validator


class ClientTransaction(BaseModel):
    datetime: datetime
    transaction_type_name: str
    value: PositiveFloat

    @validator('transaction_type_name')
    def transaction_type_allows(cls, value):
        if value not in ('deposit', 'withdraw'):
            raise ValueError('Transaction type is invalid')
        return value
