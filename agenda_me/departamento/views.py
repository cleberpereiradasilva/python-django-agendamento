from rest_framework import viewsets
from departamento.models import Department
from departamento.serializers import DepartmentSerializer

class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

