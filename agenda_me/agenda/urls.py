from django.urls import re_path, path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, DetailsView, PeriodicAgendaViewSet, RefreshAgendaView

urlpatterns = {
    re_path(r'^$', CreateView.as_view(), name="agenda"),    
    re_path(r'^(?P<pk>[0-9]+)$', DetailsView.as_view(), name="details_genda"),
    path('periodic/', PeriodicAgendaViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name="periodic_agenda"),
    path('refresh_week/', RefreshAgendaView.as_view(), name="refresh_agenda")
}
urlpatterns = format_suffix_patterns(urlpatterns)