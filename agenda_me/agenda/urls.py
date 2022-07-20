from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, DetailsView

urlpatterns = {
    re_path(r'^$', CreateView.as_view(), name="agenda"),    
    re_path(r'^(?P<pk>[0-9]+)$',
        DetailsView.as_view(), name="details_genda"),      
}
urlpatterns = format_suffix_patterns(urlpatterns)