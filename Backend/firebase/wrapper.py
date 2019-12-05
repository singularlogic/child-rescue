from django.conf import settings

# from .pyfcm.fcm import FCMNotification
from pyfcm import FCMNotification

push_service = FCMNotification(api_key=settings.FIREBASE_API_KEY)


def send_notification(
    type,
    registration_id=None,
    title=None,
    body=None,
    title_args=None,
    body_args=None,
    data=None,
):
    if type == "ios":
        push_service.notify_single_device(
            registration_id=registration_id,
            title_loc_key=title,
            body_loc_key=body,
            data_message=data,
            title_loc_args=title_args,
            body_loc_args=[body_args],
            sound="Default",
            badge=1,
        )

    else:
        data["title_loc_key"] = title
        data["title_loc_args"] = title_args
        data["body_loc_key"] = body
        data["body_loc_args"] = body_args

        push_service.single_device_data_message(
            registration_id=registration_id, data_message=data
        )  # ,android_channel_id='cr')
