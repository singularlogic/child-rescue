from rest_framework import generics
from places.models import Place
from places.web_admin_api.permissions import HasPlacePermissions
from .serializers import PlaceSerializer


class PlaceList(generics.ListCreateAPIView):
    serializer_class = PlaceSerializer
    permission_classes = (HasPlacePermissions,)

    def get_queryset(self):
        case_id = self.request.query_params.get("caseId", None)
        return Place.objects.filter(case=case_id)


class PlaceDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (HasPlacePermissions,)
