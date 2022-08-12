"""Flask Form Handler classes to but boilerplate and handle file uploads."""
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from flask import Request
from pydantic import ValidationError

from .exceptions import FilesizeLimitError, FormError
from .utils import ImageFileSaver, RequestChecker


@dataclass
class FormWithFileHandler:
    """Handle `FormModel` validation and instantiation process"""

    FormModel: Any
    request: Request
    _image_saver: ImageFileSaver = None
    _form_instance: Any = None

    @property
    def valid_form(self) -> Any:
        errors: List[Dict[str, str | Tuple]] = []
        errors = self.validate_request_and_files(errors)
        errors = self.validate_form_model(errors)
        if errors:
            raise FormError(errors=errors, model=self.FormModel)

        return self._form_instance

    def validate_request_and_files(self, errors) -> List[Dict[str, str | Tuple]]:
        try:
            RequestChecker(request=self.request)
            file_data = self.request.files["file"]
            self._image_saver = ImageFileSaver(file=file_data)
            return errors
        except ValidationError as e:
            return errors + e.errors()
        except FilesizeLimitError as e:
            errors = errors + e.errors()
            raise FormError(errors=errors, model=self.FormModel) from e

    def validate_form_model(self, errors):
        try:
            form_data = dict(self.request.form)
            self._form_instance = self.FormModel(**form_data)
            filepath = self._image_saver.save_using_uuid()
            self._form_instance.filepath = filepath
            return errors
        except ValidationError as e:
            return errors + e.errors()
