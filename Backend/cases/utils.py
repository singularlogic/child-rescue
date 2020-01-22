import os
import random
import string
import uuid
from io import StringIO, BytesIO

from PIL import Image, ExifTags
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile


class CaseUtils(object):

    PRESENCE_STATUS_CHOICES = (
        ("present", "Present"),
        ("not_present", "Not present"),
        ("transit", "Transit"),
    )
    CASE_STATUS_CHOICES = (
        ("inactive", "Inactive"),
        ("active", "Active"),
        ("closed", "Closed"),
        ("archived", "Archived"),
    )
    DISAPPEARANCE_TYPE_CHOICES = (
        ("runaway", "Runaway"),
        ("parental_abduction", "Parental Abduction"),
        ("lost", "Lost, injured or otherwise missing"),
        ("missing", "Missing UAM"),
        ("third_party_abduction", "Third-party Abduction"),
        (None, "Unknown"),
    )
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        (None, "Unknown"),
    )
    EDUCATION_CHOICES = (
        ("first_grade", "1st Grade"),
        ("second_grade", "2st Grade"),
        ("third_grade", "3st Grade"),
        (None, "Unknown"),
    )
    SKIN_COLOR_CHOICES = (
        ("light_pale", "Light Pale"),
        ("pale", "Pale"),
        ("tanned", "Tanned"),
        ("brown", "Brown"),
        ("dark_brown", "Dark Brown"),
        ("black", "Black"),
        (None, "Unknown"),
    )
    STATURE_CHOICES = (
        ("tall", "Tall"),
        ("short", "Short"),
        ("normal", "Normal"),
        (None, "Unknown"),
    )
    BODY_CHOICES = (
        ("slim", "Slim"),
        ("normal", "Normal"),
        ("overweight", "Overweight"),
        ("corpulent", "Corpulent"),
        (None, "Unknown"),
    )
    BOOLEAN_DATA_CHOICES = (
        ("yes", "Yes"),
        ("no", "No"),
        (None, "Unknown"),
    )
    MOBILE_CHOICES = (
        ("yes", "Yes"),
        ("deactivated", "Yes but deactivated or otherwise untrackable"),
        ("abductor", "Yes the abductor"),
        ("no", "No"),
        (None, "Unknown"),
    )
    BOOLEAN_POSSIBLE_DATA_CHOICES = (
        ("yes", "Yes"),
        ("possibly", "Possibly"),
        ("no", "No"),
        (None, "Unknown"),
    )
    BOOLEAN_POSSIBLE_2_DATA_CHOICES = (
        ("yes", "Yes"),
        ("probably_yes", "Probably Yes"),
        ("probably_no", "Probably No"),
        ("no", "No"),
        (None, "Unknown"),
    )
    CONCERN_CHOICES = (
        ("parent_separation", "Recent separation of parents"),
        ("on_migration", "On Migration"),
        ("parents_in_dispute", "Parents in dispute (at court or otherwise)"),
        ("physical_sexual_abuse", "Physical or Sexual abuse"),
        ("death_of_family_member", "Recent death of family member/friend"),
        ("possibly", "Possibly"),
        ("none", "None"),
        (None, "Unknown"),
    )
    DISAPPEARANCE_REASON_CHOICES = (
        ("family_issues", "Family Issues"),
        ("personal_issues", "Personal Issues"),
        ("love_affair", "Love affair"),
        ("health_issues", "Health issues"),
        ("mass_disaster", "Mass disaster"),
        ("migration", "Migration"),
        ("other", "Other"),
        (None, "Unknown"),
    )
    DISORDERS_CHOICES = (
        ("mild", "Mild"),
        ("moderate", "Moderate"),
        ("severe", "Severe, self-threatening"),
        ("none", "None"),
        (None, "Unknown"),
    )
    LIVING_ENVIRONMENT_CHOICES = (
        ("single_bio_parent", "Living with 1 biological parent"),
        ("both_bio_parents", "Living with both biological parents"),
        ("bio_step_parents", "Living with 1 biological parent + 1 step-parent"),
        ("facility", "Living in camp/hosting facility"),
        ("relatives", "Living under relatives' care/foster family"),
        ("institution", "Living in institution /psychiatric facility"),
        ("transit", "In transit"),
        (None, "Unknown"),
    )
    PARENTS_PROFILE_CHOICES = (
        ("father_step_father", "Father/Stepfather"),
        ("mother_stepmother", "Mother/Stepmother"),
        ("both", "Both"),
        ("none", "None"),
        (None, "Unknown"),
    )
    SCHOOL_GRADES_CHOICES = (
        ("excellent", "Excellent"),
        ("good", "Good"),
        ("average", "Sufficient"),
        ("not_good", "Not good"),
        ("bad", "Bad"),
        (None, "Unknown"),
    )
    RELATIONSHIP_STATUS_CHOICES = (
        ("single", "Single"),
        ("in_relationship", "In a relationship"),
        ("complicated", "It's complicated"),
        ("broke_up", "Recently broke up"),
        ("other", "Other"),
        (None, "Unknown"),
    )
    LEGAL_STATUS_CHOICES = (
        ("illegal", "No papers/Illegal"),
        ("temp_papers", "Temporal papers"),
        ("asylum_granted", "Asylum granted"),
        ("asylum_applied", "Asylum applied"),
        ("legal", "Legal"),
        (None, "Unknown"),
    )
    FOLLOWERS_CHOICES = (
        ("low", "Low < 50"),
        ("medium", "Medium < 500"),
        ("high", "High < 3000"),
        ("influencer", "Influencer < 10000"),
        (None, "Unknown"),
    )
    RECENT_ACTIVITY_CHOICES = (
        ("daily", "Daily"),
        ("frequently", "Frequently"),
        ("infrequent", "Infrequent"),
        ("inactive", "Inactive"),
        (None, "Unknown"),
    )

    @staticmethod
    def file_image_path(instance, filename):
        path = "files/case_{}/{}".format(instance.case.id, filename)
        return path

    @staticmethod
    def feed_image_path(instance, filename):
        path = "feed/case_{}/{}".format(instance.case.id, filename)
        return path

    @staticmethod
    def file_path(instance, filename):
        path = "files/case_{}/{}".format(instance.case.id, filename)
        return path

    @staticmethod
    def case_image_path(instance, filename):
        random_string = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
        path = "cases/{}/{}.jpg".format(instance, random_string)
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
            img_name += CaseUtils.get_random_string(8)
            img_name += img_ext

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

            # img.thumbnail((480, 480), Image.ANTIALIAS)
            thumb_io = BytesIO()
            if img_ext.upper() == ".JPG":
                img_ext = "JPEG"
            else:
                img_ext = img_ext.upper()[1:]
            img.save(thumb_io, format=img_ext)

            thumb_file = InMemoryUploadedFile(
                ContentFile(thumb_io.getvalue()), None, img_name, "image/*", os.sys.getsizeof(thumb_io), None,
            )
            return thumb_file
        except Exception as ex:
            print(ex)
