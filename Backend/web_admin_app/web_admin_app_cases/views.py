from rest_framework import status, permissions, generics

from rest_framework.response import Response

from core.cases.models import Case
from .serializers import CaseSerializer


class CaseList(generics.ListCreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        def _has_rights():
            if request.user.role is not None and request.user.role in ['admin', 'owner', 'coordinator', 'case_manager', 'network_manager', 'facility_manager']:
                return True
            else:
                return False

        if not _has_rights():
            return Response('User has not an admin role', status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        demographic_data = self.request.data['demographic_data'] if 'demographic_data' in self.request.data else None
        medical_data = self.request.data['medical_data'] if 'medical_data' in self.request.data else None
        social_data = self.request.data['social_data'] if 'social_data' in self.request.data else None
        physical_data = self.request.data['physical_data'] if 'physical_data' in self.request.data else None
        profile_data = self.request.data['profile_data'] if 'profile_data' in self.request.data else None

        serializer.save(demographic_data=demographic_data, medical_data=medical_data, social_data=social_data,
                        physical_data=physical_data, profile_data=profile_data)


class CaseDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        def _has_rights():
            if request.user.role is not None and request.user.role in ['admin', 'owner', 'coordinator', 'case_manager', 'network_manager', 'facility_manager']:
                return True
            else:
                return False

        if not _has_rights():
            return Response('User has not an admin role', status=status.HTTP_403_FORBIDDEN)

        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid()
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        demographic_data = self.request.data['demographic_data'] if 'demographic_data' in self.request.data else None
        medical_data = self.request.data['medical_data'] if 'medical_data' in self.request.data else None
        social_data = self.request.data['social_data'] if 'social_data' in self.request.data else None
        physical_data = self.request.data['physical_data'] if 'physical_data' in self.request.data else None
        profile_data = self.request.data['profile_data'] if 'profile_data' in self.request.data else None

        serializer.save(demographic_data=demographic_data, medical_data=medical_data, social_data=social_data,
                        physical_data=physical_data, profile_data=profile_data)
