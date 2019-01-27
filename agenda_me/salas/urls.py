from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, DetailsView
from rest_framework import routers

urlpatterns = {    
    url(r'^$', CreateView.as_view(), name="create_sala"),
    url(r'^(?P<pk>[0-9]+)$',
        DetailsView.as_view(), name="details_sala")
    
}

urlpatterns = format_suffix_patterns(urlpatterns)