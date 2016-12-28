from django.conf.urls import url
from metars import views

urlpatterns = [
  url(r'^metar/decode/$', views.DecodeMetar.as_view()),
  url(r'^metar/decode/(?P<airport_id>[A-Za-z0-9]+)/$', views.RetrieveAndDecodeMetar.as_view()),
]
