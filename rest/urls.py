# coding=utf-8
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest.views import MeasureViewSet, SensorViewSet

router = routers.DefaultRouter()

router.register(r'measures', MeasureViewSet, base_name='measures')
router.register(r'sensors', SensorViewSet, base_name='sensors')

urlpatterns =[
    path(r'', include(router.urls)),
]