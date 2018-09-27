# coding=utf-8
from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from rest.views import MeasureViewSet, SensorViewSet, get_consumption, RoomViewSet

router = routers.DefaultRouter()

router.register(r'measures', MeasureViewSet, base_name='measures')
router.register(r'sensors', SensorViewSet, base_name='sensors')
router.register(r'rooms', RoomViewSet, base_name='rooms')

urlpatterns =[
    path(r'', include(router.urls)),
    path(r'get_consumption/', get_consumption)
]