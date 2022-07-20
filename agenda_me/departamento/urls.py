from django.urls import path
from departamento.views import DepartmentViewset
from rest_framework import routers

departamento_routes = routers.DefaultRouter()

departamento_routes.register('', DepartmentViewset, basename="department_viewset")