from django.db.models import Q

from .models import Uuid, UuidActivity


class UuidManagement(object):
    @staticmethod
    def log_action(request, uuid, action="", params="", device=""):
        user = request.user if request.user.is_authenticated else None
        if user is not None:
            uuid_instance = Uuid.objects.filter(Q(value=uuid) | Q(user=user)).first()
        else:
            uuid_instance = Uuid.objects.filter(value=uuid).first()

        if uuid_instance is None:
            uuid_instance = Uuid.objects.create(value=uuid, user=user)
        else:
            uuid_instance.value = uuid

            if user is not None:
                uuid_instance.user = user

            uuid_instance.save()

        UuidActivity.objects.create(
            uuid=uuid_instance, action=action, params=params, device=device
        )
