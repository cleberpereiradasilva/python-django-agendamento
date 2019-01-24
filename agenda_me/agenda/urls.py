from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView

urlpatterns = {
    url(r'^', CreateView.as_view(), name="create_agenda"),
}

urlpatterns = format_suffix_patterns(urlpatterns)