"""Flask Form Handler classes to but boilerplate and handle file uploads."""
from dataclasses import Field, dataclass
from typing import Any, Dict, List, Tuple

from flask import Request, current_app
from pydantic import ValidationError

from .exceptions import FilesizeLimitError, FormError
from .utils import ImageFileSaver, RequestChecker


class FormWithFileHandler:
    """Handle `FormModel` validation and instantiation process"""

    def __init__(self, FormModel: Any, request: Request, basepath: str):
        self.FormModel: Any = FormModel
        self.request: Request = request
        self.basepath: str = basepath
        self._image_saver: ImageFileSaver = None
        self._form_instance: Any = None
        self._errors: List[Dict[str, str | Tuple]] = []

        # validate
        self._validate_request_and_files()
        self._validate_form_model()
        self._save_img()
        if self._errors:
            raise FormError(errors=self._errors, model=self.FormModel)

    def get_valid_form(self) -> Any:
        return self._form_instance

    def _validate_request_and_files(self):
        try:
            RequestChecker(file=self.request)
            file_data = self.request.files["file"]
            if file_data.filename:
                self._image_saver = ImageFileSaver(file=file_data)
        except ValidationError as e:
            self._errors = self._errors + e.errors()
        except FilesizeLimitError as e:
            self._errors = self._errors + e.errors()
            raise FormError(errors=self._errors, model=self.FormModel) from e

    def _validate_form_model(self):
        try:
            form_data = dict(self.request.form)
            self._form_instance = self.FormModel(**form_data)
        except ValidationError as e:
            self._errors = self._errors + e.errors()

    def _save_img(self):
        # TODO check if this is not bad practice: in loc mocking
        if self._image_saver:
            if current_app.config["TESTING"]:
                filename = "mocked_file_name.jpg"
            else:
                filename = self._image_saver.save_using_uuid(basepath=self.basepath)
            self._form_instance.file = filename
