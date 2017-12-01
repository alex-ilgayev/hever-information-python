from django.conf.urls import url, include
from rest_framework import routers
from geo_report import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    # url(r'^/$', views.UnitList.as_view()),
    url(r'^$', views.GeoReportList.as_view()),
    # url(r'^geo_report-entries/$', views.ReportEntryList.as_view()),
    # url(r'^geo_report-entries/(?P<pk>[0-9]+)/$', views.ReportEntryDetail.as_view()),
    # url(r'^reports/$', views.ReportList.as_view()),
    # url(r'^reports/today/$', views.ReportToday.as_view()),
    # url(r'^reports/(?P<pk>[0-9]+)/$', views.ReportDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
