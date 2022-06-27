from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveFloat, validator


class ClientTransaction(BaseModel):
    datetime: datetime
    transaction_type: str
    value: PositiveFloat
    pending: bool = False
    
    @validator('transaction_type')
    def transaction_type_allows(cls, value):
        if value not in ('deposit', 'withdraw'):
            raise ValueError('Transaction type is invalid')
        return value

    @validator('datetime')
    def date_time_default(cls, value):
        return datetime.strftime(value, "%Y-%m-%d %H:%M:%S")
