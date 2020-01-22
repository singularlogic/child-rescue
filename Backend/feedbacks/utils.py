import random
import string


class FeedbackUtils:
    @staticmethod
    def feedback_image_path(instance, filename):
        random_string = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
        path = "feedback_images/case_{}/{}.jpg".format(instance.case.id, random_string)
        return path
