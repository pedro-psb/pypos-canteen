
from typing import Optional
from pydantic import BaseModel


class Foo(BaseModel):
    id: Optional[int]
    name: str


a = Foo(name='foo')
print(a)
