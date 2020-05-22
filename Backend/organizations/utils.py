import os
import random
import string
import uuid
from io import StringIO, BytesIO

from PIL import Image, ExifTags
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile


class OrganizationUtils(object):
    @staticmethod
    def logo_path(instance, filename):
        random_string = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(32)
        )
        path = "organizations/{}/{}.jpg".format(instance, random_string)
        return path

    @staticmethod
    def get_random_string(N):

        random = str(uuid.uuid4())  # Convert UUID format to a Python string.
        random = random.upper()  # Make all characters uppercase.
        random = random.replace("-", "")  # Remove the UUID '-'.
        return random[0:N]

    @staticmethod
    def save_image(image):
        try:
            img = Image.open(image)

            (img_name, img_ext) = os.path.splitext(image.name)

            # Add a random string of length 8 at the end of the image to make it unique
            img_name += OrganizationUtils.get_random_string(8)
            img_name += ".jpg"
            # if hasattr(img, '_getexif'):  # only present in JPEGs
            #     for orientation in ExifTags.TAGS.keys():
            #         if ExifTags.TAGS[orientation] == 'Orientation':
            #             break
            #     e = img._getexif()  # returns None if no EXIF data
            #
            #     if e is not None:
            #         exif = dict(e.items())
            #         orientation = exif[orientation]
            #
            #         if orientation == 3:
            #             img = img.transpose(Image.ROTATE_180)
            #         elif orientation == 6:
            #             img = img.transpose(Image.ROTATE_270)
            #         elif orientation == 8:
            #             img = img.transpose(Image.ROTATE_90)

            img.thumbnail((480, 480), Image.ANTIALIAS)
            thumb_io = BytesIO()
            img.save(thumb_io, format="JPEG")

            thumb_file = InMemoryUploadedFile(
                ContentFile(thumb_io.getvalue()),
                None,
                img_name,
                "image/jpeg",
                os.sys.getsizeof(thumb_io),
                None,
            )

            return thumb_file

        except Exception as ex:
            print(ex)
