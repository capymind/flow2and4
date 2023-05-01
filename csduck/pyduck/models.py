"""
This is the module for defining ORMs and tables related to pyduck globally.
"""

from sqlalchemy.orm import Mapped


class ImageUploadMixin:
    """Represent image upload mixin."""

    url: Mapped[str]
    filename: Mapped[str]
    original_filename: Mapped[str]
    mimetype: Mapped[str | None]
    filesize: Mapped[int | None]
