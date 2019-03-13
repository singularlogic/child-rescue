from rest_framework import permissions, generics

from core.evidences.models import Evidence
from mobile_app.mobile_app_evidences.permissions import HasMobileEvidencePermission
from .serializers import EvidenceSerializer


class EvidenceList(generics.ListCreateAPIView):
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer
    permission_classes = (HasMobileEvidencePermission, )


class EvidenceDetails(generics.RetrieveAPIView):
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer
    permission_classes = (HasMobileEvidencePermission,)
