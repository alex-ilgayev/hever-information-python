from django.conf.urls import url, include
from rest_framework import routers
from account import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^signup/$', views.create_user),
    url(r'^signin/$', views.signin),
    url(r'^create_group/$', views.create_group),

]

urlpatterns = format_suffix_patterns(urlpatterns)