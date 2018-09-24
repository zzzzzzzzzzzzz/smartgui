# coding=utf-8
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import detail_route, list_route, api_view, action
from rest_framework.exceptions import APIException, ParseError
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

# Create your views here.
from rest.models import Measure, Sensor
from rest.serializers import MeasureSerializer, SensorSerializer


class MeasureViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    serializer_class = MeasureSerializer

    def get_queryset(self):
        now = datetime.now()

        timestamp_from = now - timedelta(hours=1)
        timestamp_to = now
        # временно, так как база устаревшая
        d = timedelta(days=10)
        timestamp_from -= d
        timestamp_to -= d
        return Measure.objects.filter(
            timestamp__gte=timestamp_from,
            timestamp__lt=timestamp_to,
        )

    @action(methods=['get'], detail=False)
    def get_measure_by_name(self, request):
        sensor = 'TC'
        if 'sensor' in request.GET:
            sensor = request.GET['sensor']
        qs = self.get_queryset()
        qs = qs.filter(sensor__name=sensor.upper())
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def insert_by_sensor_name(self, request):
        data = request.data
        sensor = data.get('sensor', None)
        value = data.get('value', None)
        tsp = data.get('timestamp', None)
        if sensor and value and tsp:
            try:
                snsr = Sensor.objects.get(name=sensor)
            except Sensor.DoesNotExist:
                raise APIException("I don't know such sensor") # in the future maybe it's better to just add unknown sensors
            m_obj = Measure(value=value, timestamp=tsp, sensor=snsr)
            m_obj.save()
            return HttpResponse(status=status.HTTP_200_OK)

        raise APIException("You didn't provide one of the values")


class SensorViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    serializer_class = SensorSerializer

    queryset = Sensor.objects.all()
