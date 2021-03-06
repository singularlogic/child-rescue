from rest_framework import generics
from rest_framework.views import APIView

from places.models import Place
from cases.models import Case
from places.web_admin_api.permissions import HasPlacePermissions
from .serializers import PlaceSerializer
import analytics.analytics_case as ac
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response


class EventPlaceList(generics.ListCreateAPIView):
    serializer_class = PlaceSerializer
    permission_classes = (HasPlacePermissions,)

    def get_queryset(self):
        case_id = self.request.query_params.get("caseId", None)
        return Place.objects.filter(case=case_id, is_event=True)


class ConvertToPlace(APIView):
    permission_classes = (
        HasPlacePermissions,
    )

    @staticmethod
    def post(request, *args, **kwargs):
        place_id = kwargs.pop("pk", None)
        place = get_object_or_404(Place, id=place_id)
        place.is_event = False
        place.save()
        return Response(status=status.HTTP_200_OK)


class PlaceList(generics.ListCreateAPIView):
    serializer_class = PlaceSerializer
    permission_classes = (HasPlacePermissions,)

    def get_queryset(self):
        case_id = self.request.query_params.get("caseId", None)
        case = get_object_or_404(Case, id=case_id)
        if case.status != "archived" and case.status != "closed":
            ceng = ac.ProfileEvalEngine(case)
            ceng.evaluate_fact_places()
            ceng.evaluate_non_fact_places()
        return Place.objects.filter(case=case_id, is_event=False)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        case = get_object_or_404(Case, id=data["case"])
        ceng = ac.ProfileEvalEngine(case)
        ceng.evaluate_fact_places()
        ceng.evaluate_non_fact_places()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PlaceDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (HasPlacePermissions,)
