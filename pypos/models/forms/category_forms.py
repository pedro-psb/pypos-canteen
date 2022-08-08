from typing import Dict, Optional

from pydantic import BaseModel, PrivateAttr, root_validator, validator
from pypos.models import dao_products


class AddCategoryForm(BaseModel):
    name: str
    description: Optional[str] = ""

    @validator("name")
    def unique_name(cls, value):
        category = dao_products.get_category_by_name(value)
        if category:
            raise ValueError("Category name already taken")
        return value

    class Config:
        anystr_strip_whitespace = True


class UpdateCategoryForm(AddCategoryForm):
    category_id: int
    _original_category: Dict = PrivateAttr()

    @root_validator
    def category_id_exist(cls, values):
        original_category = dao_products.get_category_by_id(values["category_id"])
        if not original_category:
            raise ValueError("Product id is invalid")
        values["_original_category"] = original_category
        return values

    @validator("name")
    def unique_name(cls, value):
        return value

    @root_validator
    def unique_name_except_original(cls, values):
        category_update = dao_products.get_category_by_name(values["name"])
        original_name = values["_original_category"]["name"]
        if category_update:
            if category_update["name"] != original_name:
                raise ValueError("Product should have a unique name")
        return values

    class Config:
        anystr_strip_whitespace = True
