from rest_framework import permissions, generics

from core.alerts.models import Alert
from web_admin_app.web_admin_app_alerts.serializers import AlertSerializer


class AlertList(generics.ListCreateAPIView):
    serializer_class = AlertSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        case_id = self.request.query_params.get('case_id', None)
        active = self.request.query_params.get('active', None)

        # if active is not None:
        #     queryset = Alert.objects.is_active()
        # else:
        #     queryset = Alert.objects.all()
        #
        # if case_id is not None:
        #     result = []
        #     for item in queryset:
        #         if str(item.case_id) == str(case_id):
        #             result.append(item)
        #     queryset = result

        return Alert.objects.get_web_queryset(active, case_id)


class AlertDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = (permissions.IsAuthenticated,)
