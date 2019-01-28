from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, DetailsView

urlpatterns = {
    url(r'^$', CreateView.as_view(), name="create_agenda"),
    url(r'^(?P<pk>[0-9]+)$',
        DetailsView.as_view(), name="details_genda"),    
}
urlpatterns = format_suffix_patterns(urlpatterns)