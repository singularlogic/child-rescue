from rest_framework import permissions, generics

from core.choices.models import SchoolGrades
from web_admin_app.web_admin_app_choices.serializers import SchoolGradesSerializer


class SchoolGradesList(generics.ListCreateAPIView):
    queryset = SchoolGrades.objects.all()
    serializer_class = SchoolGradesSerializer
    permission_classes = (permissions.IsAuthenticated,)


class SchoolGradesDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = SchoolGrades.objects.all()
    serializer_class = SchoolGradesSerializer
    permission_classes = (permissions.IsAuthenticated,)
