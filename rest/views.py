# coding=utf-8
from datetime import datetime, timedelta

from django.db import connection
from django.http import HttpResponse
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# Create your views here.
from rest.models import Measure, Sensor, Room
from rest.serializers import MeasureSerializer, SensorSerializer, RoomSerializer


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
        room_name = '403'
        if 'room_name' in request.GET:
            room_name = request.GET['room_name'].lower()
        qs = self.get_queryset()
        qs = qs.filter(sensor__name=sensor.upper(), room__name=room_name)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def insert_by_sensor_name(self, request):
        data = request.data
        sensor = data.get('sensor', None)
        value = data.get('value', None)
        tsp = data.get('timestamp', None)
        room_name = data.get('room_name', None)
        if sensor and value and tsp and room_name:
            try:
                snsr = Sensor.objects.get(name=sensor)
            except Sensor.DoesNotExist:
                raise APIException(
                    "I don't know such sensor")  # in the future maybe it's better to just add unknown sensors
            try:
                room = Room.objects.get(name=room_name.lower())
            except Room.DoesNotExist:
                raise APIException(
                    "I don't know such room")  # in the future maybe it's better to just add unknown rooms
            m_obj = Measure(value=value, timestamp=tsp, sensor=snsr, room=room)
            m_obj.save()
            return HttpResponse(status=status.HTTP_200_OK)

        raise APIException("You didn't provide one of the values")


class SensorViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    serializer_class = SensorSerializer

    queryset = Sensor.objects.all()


class RoomViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    serializer_class = RoomSerializer

    queryset = Room.objects.all()


MONTHS = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}


@api_view(['GET'])
def get_consumption(request):
    consumer = 'RADIATOR_VAL1'
    if 'consumer' in request.GET:
        consumer = request.GET['consumer'].upper()

    room_name = '403'
    if 'room_name' in request.GET:
        room_name = request.GET['room_name'].lower()

    try:
        with connection.cursor() as cursor:
            query = \
                """
                        SELECT
                            sensor_id as id,
                            sensor_name,
                            room_name,
                            round(consumption / (0.3*3600), 2) as number_kw_on_h,
                            round((consumption / (0.3*3600)) * 5.38, 2) as amount_of_money,
                            mth as month
                        FROM
                            (SELECT
                                --kilowatt*fraction_of_usage*number_of_seconds_used
                                --fraction_of_usage is the part of time when the value was 1.0
                                (0.3*summary_on/cnt)*(CAST(strftime('%s', max_date) as integer)-CAST(strftime('%s',min_date) as integer)) as consumption,
                                mth,
                                sensor_id,
                                sensor_name,
                                room_name
                            FROM
                                (SELECT 
                                    SUM(rest_measure.value) as summary_on,
                                    COUNT(*) as cnt,
                                    rest_sensor.id as sensor_id,
                                    rest_sensor.name as sensor_name,
                                    rest_room.name as room_name,
                                    MAX(rest_measure.timestamp) as max_date,
                                    MIN(rest_measure.timestamp) as min_date,
                                    strftime('%m', rest_measure.timestamp) as mth
                                FROM 
                                    rest_measure
                                    INNER JOIN
                                    rest_sensor
                                    ON
                                    rest_measure.sensor_id = rest_sensor.id
                                    INNER JOIN
                                    rest_room
                                    ON
                                    rest_measure.room_id = rest_room.id
                                WHERE
                                    timestamp BETWEEN (SELECT min(timestamp) FROM rest_measure) AND (SELECT max(timestamp) FROM rest_measure)
                                    AND UPPER(rest_sensor.name)='{consumer}'
                                GROUP BY mth, rest_sensor.id, rest_sensor.name) as aggregated) as cons
                        """.format(consumer=consumer)

            cursor.execute(query)
            raw = cursor.fetchall()
            response = []
            for elem in raw:
                response.append(
                    {
                        'id': elem[0],
                        'sensor_name': elem[1],
                        'room_name': elem[2],
                        'number_kw_on_h': elem[3],
                        'amount_of_money': elem[4],
                        'month': MONTHS[elem[5]]
                    }
                )
            return Response(data=response, status=status.HTTP_200_OK)
    except Exception:
        return Response(data={"message": "Something went wrong, couldn't get data, try later"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
