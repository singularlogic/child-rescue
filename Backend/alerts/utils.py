import os
import uuid

from io import StringIO

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image, ExifTags


def image_path(instance, filename):
    path = "alert_images/"
    path = path + "%s" % instance.image
    return path


def save_image(image, user):
    try:
        img = Image.open(image)

        (img_name, img_ext) = os.path.splitext(image.name)

        # Add a random string of length 8 at the end of the image to make it unique
        img_name += get_random_string(8)
        img_name += ".jpg"

        if hasattr(img, "_getexif"):  # only present in JPEGs
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == "Orientation":
                    break
            e = img._getexif()  # returns None if no EXIF data

            if e is not None:
                exif = dict(e.items())
                orientation = exif[orientation]

                if orientation == 3:
                    img = img.transpose(Image.ROTATE_180)
                elif orientation == 6:
                    img = img.transpose(Image.ROTATE_270)
                elif orientation == 8:
                    img = img.transpose(Image.ROTATE_90)

        img.thumbnail((200, 200), Image.ANTIALIAS)
        thumb_io = StringIO()
        # or it is i.StringIO() - in Python2.7 it was StringIO.StringIO()
        img.save(thumb_io, format="JPEG")
        thumb_file = InMemoryUploadedFile(
            ContentFile(thumb_io.getvalue()),
            None,
            img_name,
            "image/jpeg",
            thumb_io.len,
            None,
        )
        return thumb_file
    except Exception as ex:
        print(ex)


# Function to generate a random string of length N (using uuid)
def get_random_string(n):

    random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    random = random.upper()  # Make all characters uppercase.
    random = random.replace("-", "")  # Remove the UUID '-'.
    return random[0:n]  # Return the random string.
