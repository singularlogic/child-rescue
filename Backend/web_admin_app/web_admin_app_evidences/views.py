from rest_framework import permissions, generics

from core.evidences.models import Evidence
from .serializers import EvidenceSerializer


class EvidenceList(generics.ListCreateAPIView):
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer
    permission_classes = (permissions.IsAuthenticated,)


class EvidenceDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer
    permission_classes = (permissions.IsAuthenticated,)
