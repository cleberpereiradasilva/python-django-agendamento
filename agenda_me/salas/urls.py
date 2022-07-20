from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, DetailsView
from rest_framework import routers

urlpatterns = {    
    re_path(r'^$', CreateView.as_view(), name="create_sala"),
    re_path(r'^(?P<pk>[0-9]+)$',
        DetailsView.as_view(), name="details_sala")
    
}

urlpatterns = format_suffix_patterns(urlpatterns)