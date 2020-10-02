from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings


def make_thumbnail(image, size=(120, 120)) -> ContentFile:
    """Make thumbnail."""

    file, ex = os.path.splitext(image.name.lower())
    thumb_ex = 'JPEG' if ex in ['.jpg', '.jpeg'] else 'PNG'

    img = Image.open(image)
    img.thumbnail(size, Image.ANTIALIAS)

    with BytesIO() as fileobj:
        img.save(fileobj, format=thumb_ex)
        fileobj.seek(0)
        return ContentFile(fileobj.read())


def remove_img(relative_path):
    img_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    os.remove(img_path)