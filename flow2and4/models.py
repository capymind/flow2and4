"""
This is the module for defining ORMs or tables in database related to csduck.
"""

from sqlalchemy.orm import Mapped, mapped_column
from flow2and4.database import db


class ImageUploadMixin:
    """Represent image upload mixin."""

    url: Mapped[int]
    filename: Mapped[str]
    original_filename: Mapped[str]
    filesize: Mapped[int]
    mimetype: Mapped[str]
