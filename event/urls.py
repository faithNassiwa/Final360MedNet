from django.conf.urls import url
from event import views


urlpatterns = [
    url(r'^scholarships/', views.scholarships),
    url(r'^jobs/', views.jobs),
    url(r'^events/category/(?P<category>[a-zA-Z0-9_\-]+)/$', views.event_results),
    url(r'^events/search/', views.get_events),
    url(r'^events/([0-9]+)/', views.event),
    url(r'^events/$', views.index, name='events'),
]