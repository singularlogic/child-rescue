from rest_framework import status, permissions, generics

from rest_framework.response import Response

from core.cases.models import Case
from .serializers import CaseSerializer


class CaseList(generics.ListCreateAPIView):
    serializer_class = CaseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        child_id = self.request.query_params.get('child_id', None)
        if child_id is not None:
            queryset = Case.objects.filter(child_id=child_id)
        else:
            queryset = Case.objects.all()
        return queryset

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
        psychological_data = self.request.data['psychological_data'] if 'psychological_data' in self.request.data else None
        physical_data = self.request.data['physical_data'] if 'physical_data' in self.request.data else None
        personal_data = self.request.data['personal_data'] if 'personal_data' in self.request.data else None
        social_media_data = self.request.data['social_media_data'] if 'social_media_data' in self.request.data else None

        serializer.save(demographic_data=demographic_data, medical_data=medical_data, psychological_data=psychological_data,
                        physical_data=physical_data, personal_data=personal_data, social_media_data=social_media_data)


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
        psychological_data = self.request.data['psychological_data'] if 'psychological_data' in self.request.data else None
        physical_data = self.request.data['physical_data'] if 'physical_data' in self.request.data else None
        personal_data = self.request.data['personal_data'] if 'personal_data' in self.request.data else None
        social_media_data = self.request.data['social_media_data'] if 'social_media_data' in self.request.data else None

        serializer.save(demographic_data=demographic_data, medical_data=medical_data, psychological_data=psychological_data,
                        physical_data=physical_data, personal_data=personal_data, social_media_data=social_media_data)
