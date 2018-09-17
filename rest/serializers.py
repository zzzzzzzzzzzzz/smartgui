# coding=utf-8
from rest_framework import serializers

from rest.models import Measure, Sensor


class MeasureSerializer(serializers.ModelSerializer):
    sensor_name = serializers.ReadOnlyField(source='sensor.name')

    class Meta:
        model = Measure
        fields = ('pk', 'value', 'sensor_name', 'timestamp')


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('pk', 'name', 'description')