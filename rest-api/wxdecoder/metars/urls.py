from django.conf.urls import url
from metars import views

urlpatterns = [
  url(r'^metar/(?P<pk>[A-Za-z0-9]+)/$', views.MetarDetail.as_view()),
]
