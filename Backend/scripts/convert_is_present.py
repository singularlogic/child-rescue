from cases.models import Case


def run():
    def _print_status(_item):
        print(
            "{} is_present: {}, status: {}, presence_status: {}".format(
                _item.id, _item.is_present, _item.status, _item.presence_status
            )
        )

    for item in Case.objects.all():
        if item.status == "active":
            item.presence_status = "missing"
            item.save()
            _print_status(item)
            continue
        if item.is_present is None:
            item.presence_status = ""
            item.save()
            _print_status(item)
            continue
        if item.is_present is False:
            item.presence_status = "not_present"
            item.save()
            _print_status(item)
            continue
        if item.is_present is True:
            item.presence_status = "present"
            item.save()
            _print_status(item)
            continue
