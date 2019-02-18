from rest_framework import status, permissions, generics
from rest_framework.response import Response


from .models import Case, Profile

from .serializers import CaseSerializer, ProfileSerializer


class CaseList(generics.ListCreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        child_id = self.request.data['child_id']
        serializer.save(child_id=child_id)


class CaseDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # def perform_create(self, serializer):
    #     case_id = self.request.data['case_id']
    #     serializer.save(case_id=case_id)

    def create(self, validated_data):
        profiles = validated_data.pop('profiles')
        case = Case.objects.create(**validated_data)
        for profile in profiles:
            Profile.objects.create(case=case, **profile)
        return case


class ProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

