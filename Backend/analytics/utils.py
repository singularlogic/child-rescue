from cases.models import Case
from datetime import datetime, timedelta
from calendar import monthrange


class AnalyticsUtils:
    @staticmethod
    def get_interval(case_id, group_by):
        try:
            case = Case.objects.get(pk=case_id)
        except Case.DoesNotExist:
            return None
        case_start = datetime.date(case.created_at)
        if case.status == "active":
            case_end = datetime.date(datetime.now())
        else:
            case_end = case.end_date  # needs check

        if group_by == "week":
            case_start_week = case_start - timedelta(days=case_start.weekday())
            case_end_week = case_end - timedelta(days=case_end.weekday())
            delta = case_end_week - case_start_week
            interval = int(delta.days / 7 + 1)
        elif group_by == "month":
            case_start_month = case_start.replace(day=1)
            case_end_month = case_end.replace(day=1)
            months = 0
            while True:
                mdays = monthrange(case_start_month.year, case_start_month.month)[1]
                case_start_month += timedelta(days=mdays)
                if case_start_month <= case_end_month:
                    months += 1
                else:
                    break
            interval = months + 1
        else:
            delta = case_end - case_start
            interval = delta.days
        return interval
