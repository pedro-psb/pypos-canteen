"""File Handling utilities for flask"""
import os

import shortuuid
from flask import current_app
from pydantic import BaseModel
from werkzeug import datastructures
from werkzeug.utils import secure_filename


# TODO add custom error handling for None
class FileStorage(datastructures.FileStorage):
    """Pydantic Data Type wrapper for `werkzeug.datastructures.FileStorage`"""

    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

    @classmethod
    def __get_validators__(cls):
        yield cls.file_isnt_empty
        yield cls.file_extension_is_valid

    @classmethod
    def file_isnt_empty(cls, file: datastructures.FileStorage):
        filename = file.filename
        if filename == "" or not file:
            raise ValueError("Must select a file")
        return file

    @classmethod
    def file_extension_is_valid(cls, file: datastructures.FileStorage):
        # TODO add real image validation
        file_extension = get_file_extension(file.filename)
        if file_extension in cls.ALLOWED_EXTENSIONS:  # type: ignore
            return file
        raise ValueError("Extension must be png, jpg or jpeg")


class ImageFileSaver(BaseModel):
    """Pydantic Model to handle file uploads"""

    file: FileStorage

    def save_using_uuid(self) -> str:
        """Save file using uuid4 on base56 and return the file path"""
        filepath = self.save_as(shortuuid.uuid())
        return filepath

    def save_as(self, filename: str):
        """Save file using a custom filename (extension is added automatically)"""
        file_extension = get_file_extension(self.file.filename)
        filename = secure_filename(f"{filename}.{file_extension}")
        filename = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        self.file.save(filename)
        return filename


def get_file_extension(filename: str | None) -> str | None:
    if filename and "." in filename:
        return filename.rsplit(".", 1)[1].lower()
    return None
