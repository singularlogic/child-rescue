from datetime import datetime

from django.db import models
from django.db.models import Count
from django.db.models.functions import TruncWeek, TruncMonth
from django.db.models.signals import post_save
from django.dispatch import receiver

from alerts.models import Alert
from cases.models import Case
from feedbacks.utils import FeedbackUtils
from analytics.utils import AnalyticsUtils
from organizations.models import Organization
from users.models import User, Uuid


class FeedbackSet(models.QuerySet):
    @staticmethod
    def get_latest_web_queryset(organization_id):
        if organization_id is None:
            return Feedback.objects.all().order_by("-created_at")[:5]
        else:
            return Feedback.objects.filter(organization=organization_id).order_by("-created_at")[:5]

    @staticmethod
    def get_web_query_set(organization_id, case_id, is_superuser):
        if is_superuser:
            if case_id is not None:
                queryset = Feedback.objects.filter(case=case_id).order_by("id").reverse()
            elif organization_id is not None:
                queryset = Feedback.objects.filter(organization=organization_id).order_by("id").reverse()
            else:
                queryset = Feedback.objects.all().order_by("id").reverse()
        else:
            if case_id is not None:
                queryset = Feedback.objects.filter(case=case_id).order_by("id").reverse()
            else:
                queryset = Feedback.objects.filter(organization=organization_id).order_by("id").reverse()
        return queryset

    @staticmethod
    def get_feedback_count(case_id, group_by):
        try:
            organization = Case.objects.get(pk=case_id).organization.id
        except Case.DoesNotExist:
            return None
        cases = Case.objects.filter(organization=organization)
        counts = []
        sum_average = 0
        for case in cases:
            if group_by == "week":
                queryset = list(
                    Feedback.objects.filter(case=case_id)
                    .annotate(date_field=TruncWeek("created_at"))
                    .values("date_field")
                    .annotate(count=Count("id"))
                    .order_by("date_field")
                )
                for i in range(len(queryset)):
                    queryset[i]["date_field"] = datetime.date(queryset[i]["date_field"])
            elif group_by == "month":
                queryset = list(
                    Feedback.objects.filter(case=case_id)
                    .annotate(date_field=TruncMonth("created_at"))
                    .values("date_field")
                    .annotate(count=Count("id"))
                    .order_by("date_field")
                )
                for i in range(len(queryset)):
                    queryset[i]["date_field"] = datetime.date(queryset[i]["date_field"])
            else:
                queryset = list(
                    Feedback.objects.filter(case=case_id)
                    .extra(select={"date_field": "date( created_at )"})
                    .values("date_field")
                    .annotate(count=Count("id"))
                    .order_by("date_field")
                )
            sum_case_counts = 0
            for item in queryset:
                sum_case_counts += item["count"]
            interval = AnalyticsUtils.get_interval(case.id, group_by)
            case_average = (sum_case_counts / interval) if interval > 0 else 0
            if int(case_id) == case.id:
                counts = queryset
            sum_average += case_average
        organization_average = sum_average / len(cases)
        result = {"counts": counts, "average": organization_average}
        return result


class Feedback(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="case")
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user", blank=True, null=True)
    uuid = models.ForeignKey(Uuid, on_delete=models.CASCADE, related_name="uuid", blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

    is_main = models.BooleanField(default=False)
    score = models.FloatField(default=1.0)
    source = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    current_latitude = models.FloatField(blank=True, null=True)
    current_longitude = models.FloatField(blank=True, null=True)
    comment = models.CharField(max_length=8000, blank=True, null=True)
    note = models.CharField(max_length=8000, blank=True, null=True)
    feedback_image = models.ImageField(upload_to=FeedbackUtils.feedback_image_path, blank=True, null=True)

    address = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    checked_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name="checker")
    checked_on = models.DateTimeField(blank=True, null=True)

    FEEDBACK_STATUSES = (
        ("pending", "Pending"),
        ("relevant", "Relevant"),
        ("irrelevant", "Irrelevant"),
        ("credible", "Credible"),
        ("spam", "Spam"),
    )
    feedback_status = models.CharField(max_length=256, choices=FEEDBACK_STATUSES, default="pending")
    is_valid = models.NullBooleanField()

    location_selected_reasons = models.CharField(max_length=5000, blank=True, null=True)
    CHILD_STATUS = (
        ("ok", "Ok"),
        ("appearance_change", "Appearance change (clothes, haircut, etc)"),
        ("shocked", "Terrified/Shocked"),
        ("injured_sick", "Injured/Sick/Intoxicated"),
        ("deceased", "Deceased"),
        (None, "Unknown"),
    )
    child_status = models.CharField(max_length=256, blank=True, null=True)
    TRANSPORTATION_CHOICES = (
        ("foot", "Foot"),
        ("bus_tram", "Bus/Tram"),
        ("car_motorcycle", "Car/Motorcycle"),
        ("metro_subway", "Metro/Subway"),
        ("train", "Train"),
        ("bicycle_scooter", "Bicycle/Scooter"),
        ("ship_aeroplane", "Ship/Aeroplane"),
        (None, "Unknown"),
    )
    transportation = models.CharField(max_length=256, blank=True, null=True)
    objects = FeedbackSet.as_manager()

    def __str__(self):
        return "Feedback: {id} for case {case}".format(id=self.id, case=self.case)


@receiver(post_save, sender=Feedback, dispatch_uid="notify_case_managers_for_feedback")
def notify_case_managers_for_feedback(sender, instance, **kwargs):
    case_managers = User.objects.filter(organization=instance.organization, role="case_manager")
    from django.conf import settings
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
    from django.template import loader
    from django.core.mail import send_mail

    if instance.is_main:
        return

    image = settings.BASE_FE_URL + instance.case.profile_photo.url if instance.case.profile_photo else None

    for case_manager in case_managers:
        params = {
            "email": case_manager.email,
            "base_url": settings.BASE_FE_URL,
            "case": instance.case,
            "image": image,
            "source": instance.source,
            "comment": instance.comment or " - ",
            "address": instance.address,
            "date": instance.date,
            "created_at": instance.created_at,
            "fullname": instance.case.custom_name,
            "site_name": "platform.childrescue.eu",
            "uid": urlsafe_base64_encode(force_bytes(case_manager.pk)),
            "user": case_manager,
            "token": default_token_generator.make_token(case_manager),
        }
        email_template_name = "users/feedback_notification.html"
        prefix = settings.SERVER.upper() + " " if settings.SERVER != 'production' else ""
        subject = "{}ChildRescue case #{} : Feedback provided by {}".format(prefix, instance.case.id, instance.source)
        html_content = loader.get_template(email_template_name).render(params)
        send_mail(
            subject,
            "",
            "Child Rescue <%s>" % settings.DEFAULT_FROM_EMAIL,
            [case_manager.email],
            fail_silently=False,
            html_message=html_content,
        )
