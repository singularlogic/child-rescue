from rest_framework import permissions, generics

from core.cases.models import Case
from .serializers import CaseSerializer


class CaseList(generics.ListAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CaseDetails(generics.RetrieveAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = (permissions.IsAuthenticated,)
