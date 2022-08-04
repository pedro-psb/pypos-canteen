from typing import Dict, List

from pydantic import BaseModel


def parse_errors(errors: List[Dict], model: BaseModel) -> Dict[str, List]:
    """Format errors from errors.loc[fields] to [field.error]"""
    # TODO fix typecheck error in the parameters
    # get fields from pydantic datamodel
    model_schema = model.schema()["properties"]
    # add to forms dict
    form_dict = {}
    for field in model_schema:
        form_dict[field] = []
        for error in errors:
            if field in error["loc"]:
                form_dict[field].append(error["msg"])
    return form_dict
