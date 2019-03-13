from django.db.models import IntegerField, Value, Q
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from core.cases.models import Case
from .serializers import CaseSerializer


class CaseList(generics.ListAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    #
    # def list(self, request, *args, **kwargs):
    #     latitude = self.request.query_params.get('latitude', None)
    #     longitude = self.request.query_params.get('longitude', None)
    #
    #     if latitude is None or longitude is None:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     return super(CaseList, self).list(request, args, kwargs)
    #
    # def get_queryset(self):
    #     latitude = self.request.query_params.get('latitude', None)
    #     longitude = self.request.query_params.get('longitude', None)
    #
    #     queryset = Case.objects.annotate(
    #         distance=Distance(
    #             'geolocation_point',
    #             Point(float(latitude), float(longitude), srid=4326)
    #         )).order_by('distance')[:2]
    #
    #     result = []
    #     for item in queryset:
    #         print(item.radius)
    #         print(item.distance.km)
    #         if int(item.distance.km) <= item.radius:
    #             result.append(item)
    #
    #     return result


class CaseDetails(generics.RetrieveAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    # permission_classes = (permissions.IsAuthenticated,)
