"""File Handling utilities for flask"""
import os
from typing import Any, Optional, Set

import shortuuid
from flask import Request, current_app
from pydantic import BaseModel, root_validator, validator
from werkzeug import datastructures
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from .exceptions import FilesizeLimitError


class RequestChecker(BaseModel):
    """Pydantic Model to validate `flask.Request`, in particular the `request.files` field."""

    file: Request
    _ALLOWED_EXTENSIONS: Set = {"png", "jpg", "jpeg"}

    # TODO move this validation to the Fileupload form, as it is related with field validation choices
    @validator("file")
    @classmethod
    def check_file_limit(cls, request: Request):
        try:
            request.files["file"].filename
        except RequestEntityTooLarge as e:
            raise FilesizeLimitError(loc="file") from e
        return request

    @validator("file")
    @classmethod
    def file_extension_is_valid(cls, request: Request):
        # TODO add real image validation
        filename = request.files["file"].filename
        file_extension = get_file_extension(filename)
        if filename:
            if file_extension in cls._ALLOWED_EXTENSIONS:  # type: ignore
                return request
            raise TypeError("Extension must be png, jpg or jpeg")
        return request

    class Config:
        arbitrary_types_allowed = True


class ImageFileSaver(BaseModel):
    """Pydantic Model to handle file uploads"""

    file: datastructures.FileStorage

    def save_using_uuid(self, basepath: str) -> str:
        """Save file using uuid4 on base56 and return the file path"""
        filename = self.save_as(filename=shortuuid.uuid(), basepath=basepath)
        return filename

    def save_as(self, filename: str, basepath: str):
        """Save file using a custom filename (extension is added automatically)"""
        file_extension = get_file_extension(self.file.filename)
        filename = secure_filename(f"{filename}.{file_extension}")
        filepath = os.path.join("pypos", basepath, filename)
        self.file.save(filepath)
        return filename

    class Config:
        arbitrary_types_allowed = True


def get_file_extension(filename: str | None) -> str | None:
    if filename and "." in filename:
        return filename.rsplit(".", 1)[1].lower()
    return None
