# coding=utf-8
from django.db import models
from django.db.models import Func


# Create your models here.
class Room(models.Model):
    class Meta:
        verbose_name = u"Комната"
        verbose_name_plural = u"Комнаты"

    name = models.CharField(
        verbose_name=u"Название комнаты",
        blank=False,
        null=False,
        max_length=255,
        unique=True,
    )

    description = models.TextField(
        verbose_name=u"Описание комнаты, что там находится, итп",
        blank=False,
        null=False,
    )


class Sensor(models.Model):
    class Meta:
        verbose_name = u"Сенсор"
        verbose_name_plural = u"Сенсоры"

    name = models.CharField(
        verbose_name=u"Имя сенсора",
        blank=False,
        null=False,
        max_length=255,
        unique=True,
    )

    description = models.TextField(
        verbose_name=u"Описание отображаемой информации",
        blank=False,
        null=False,
    )


class Measure(models.Model):
    class Meta:
        ordering = ["timestamp"]
        verbose_name = "Значение сенсора"
        verbose_name_plural = "Значение сенсора"

    def __str__(self):
        return "{0.sensor.name} | {0.value}".format(self)

    room = models.ForeignKey(
        Room,
        default=1,
        related_name='room',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Комната",
        help_text="Идентификатор комнаты в которой находится датчик, и откуда пришло измерение"
    )

    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.SET_NULL,
        default=1,
        related_name='sensor',
        null=True,
        blank=True,
        verbose_name="Сенсор/Счётчик/Датчик",
        help_text="Источник информации",
    )

    value = models.FloatField(
        default=0.0,
        null=False,
        blank=False,
        verbose_name=u"Значение"
    )

    timestamp = models.DateTimeField(
        verbose_name="Время",
    )


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()
